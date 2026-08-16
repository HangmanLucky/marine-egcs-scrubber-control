(*
====================================================================================
  PROJECT   : Smart Exhaust Gas Cleaning System (EGCS)
              Automated Closed-Loop Scrubber Control
  MODULE    : FB_EGCS_ScrubberControl
  PLATFORM  : IEC 61131-3 Structured Text
              Written against Siemens SCL (TIA Portal, S7-1500) syntax,
              portable to CODESYS-based marine automation platforms
              (e.g. Kongsberg AIM / Wartsila engine room controllers)
              with minor FB-instance renaming.
  AUTHOR    : Sipho Lucky Sibanda
  CONTEXT   : Open-loop scrubber wash-water is dosed with an alkaline
              solution (typically NaOH) to neutralise SOx absorbed from
              main/auxiliary engine exhaust before the water is either
              discharged overboard or held for treatment.

  REGULATORY BASIS (simulated against, for realism only - not certified):
    - MARPOL Annex VI, Regulation 14  : Global 0.50% m/m sulphur cap,
                                         0.10% m/m inside Emission Control
                                         Areas (ECAs) unless an approved
                                         EGCS is used.
    - IMO MEPC.259(68) 2015 Guidelines: Discharge water pH >= 6.5 measured
                                         at overboard discharge (or a
                                         maximum 12 pH-unit difference vs
                                         intake, whichever is less strict).
====================================================================================
*)

TYPE ST_EmissionRecord :
STRUCT
    Timestamp        : DT;         // Date/time of log entry
    pH_Value          : REAL;       // Discharge water pH at time of log
    SOx_ppm           : REAL;       // Exhaust SOx concentration, ppm
    DoseRate_Pct      : REAL;       // Dosing pump output at time of log
    DischargeActive   : BOOL;       // TRUE if wash water was being discharged
    InECA             : BOOL;       // Vessel position flag at time of log
END_STRUCT
END_TYPE

FUNCTION_BLOCK FB_EGCS_ScrubberControl
VAR_INPUT
    pH_Feedback         : REAL;     // 4-20mA pH probe, scaled 0.00 - 14.00
    SOx_ppm             : REAL;     // Exhaust gas SOx analyser, ppm
    ExhaustTemp_C       : REAL;     // Exhaust gas temperature, deg C
    GPS_InECA           : BOOL;     // TRUE when vessel position (from
                                     // navigation system) is inside a
                                     // designated Emission Control Area
    System_Enable       : BOOL;     // Master enable from bridge/ECR HMI
    Sensor_Fault        : BOOL;     // TRUE if pH or SOx sensor reports
                                     // out-of-range / comms fault
END_VAR

VAR_OUTPUT
    AlkalineDosingPump_Speed : REAL := 0.0;   // 0-100% VFD speed reference
    WashWaterDischargeValve  : BOOL := FALSE; // TRUE = permitted to open
    Alarm_HighSOx            : BOOL := FALSE;
    Alarm_LowpH              : BOOL := FALSE;
    Alarm_ECA_Lockout        : BOOL := FALSE;
    Alarm_SensorFault        : BOOL := FALSE;
    SystemStatus             : STRING[20] := 'STANDBY';
END_VAR

VAR
    // --- Setpoints / regulatory limits ---
    pH_Setpoint          : REAL := 6.50;   // MEPC.259(68) minimum discharge pH
    pH_LowLow            : REAL := 6.00;   // Hard trip - forces valve closed
    SOx_Limit_ppm         : REAL := 11.50; // Approx. equivalent to 0.10% S in ECA
    SOx_HighHigh          : REAL := 14.00; // Hard alarm threshold

    // --- PID tuning (alkaline dosing pump speed vs pH deviation) ---
    PID_Inst              : FB_PID;         // Standard vendor PID instance
    Kp                     : REAL := 8.0;
    Ti_s                   : REAL := 20.0;   // Integral time, seconds
    Td_s                    : REAL := 0.0;
    PID_Output             : REAL;

    // --- Logging ---
    EmissionLog            : ARRAY[0..999] OF ST_EmissionRecord;
    LogIndex                : INT := 0;
    LogTimer                : TON;           // Log every 60s while running
    LogTimer_PT             : TIME := T#60S;

    // --- Internal ---
    DischargePermitted     : BOOL;
END_VAR

// ------------------------------------------------------------------
// 1. SENSOR / COMMS FAULT HANDLING - fails to safe state
// ------------------------------------------------------------------
IF Sensor_Fault THEN
    Alarm_SensorFault        := TRUE;
    AlkalineDosingPump_Speed := 0.0;
    WashWaterDischargeValve  := FALSE;
    SystemStatus              := 'SENSOR FAULT';
    RETURN;
ELSE
    Alarm_SensorFault := FALSE;
END_IF

// ------------------------------------------------------------------
// 2. REGULATORY / ECA GPS INTERLOCK
//    Wash water discharge is never permitted while the vessel's
//    navigation system reports it is inside a restricted / no-discharge
//    Emission Control Area, regardless of pH/SOx compliance.
// ------------------------------------------------------------------
Alarm_ECA_Lockout := GPS_InECA;
DischargePermitted := System_Enable AND NOT GPS_InECA AND NOT Sensor_Fault;

// ------------------------------------------------------------------
// 3. CLOSED-LOOP pH CONTROL (PID)
//    Increases alkaline dosing pump speed as pH drifts below setpoint.
// ------------------------------------------------------------------
IF System_Enable THEN
    PID_Inst(
        SP       := pH_Setpoint,
        PV       := pH_Feedback,
        KP       := Kp,
        TI       := Ti_s,
        TD       := Td_s,
        MANUAL   := FALSE,
        LMN_HLM  := 100.0,
        LMN_LLM  := 0.0
    );
    PID_Output := PID_Inst.LMN;

    // Hard trip below pH_LowLow: force max dosing regardless of PID ramp
    IF pH_Feedback <= pH_LowLow THEN
        AlkalineDosingPump_Speed := 100.0;
    ELSE
        AlkalineDosingPump_Speed := PID_Output;
    END_IF
ELSE
    AlkalineDosingPump_Speed := 0.0;
    PID_Inst(MANUAL := TRUE, LMN := 0.0);
END_IF

// ------------------------------------------------------------------
// 4. ALARM EVALUATION
// ------------------------------------------------------------------
Alarm_LowpH   := (pH_Feedback < pH_Setpoint) AND System_Enable;
Alarm_HighSOx := (SOx_ppm > SOx_Limit_ppm);

// ------------------------------------------------------------------
// 5. DISCHARGE VALVE PERMISSIVE
//    Valve only opens if: system enabled, NOT in ECA, pH within limit,
//    SOx within limit, no sensor fault.
// ------------------------------------------------------------------
WashWaterDischargeValve := DischargePermitted
                            AND (pH_Feedback >= pH_Setpoint)
                            AND (SOx_ppm <= SOx_HighHigh);

// ------------------------------------------------------------------
// 6. SYSTEM STATUS TEXT (drives HMI banner)
// ------------------------------------------------------------------
IF NOT System_Enable THEN
    SystemStatus := 'STANDBY';
ELSIF GPS_InECA THEN
    SystemStatus := 'ECA - DISCHARGE LOCKED';
ELSIF Alarm_HighSOx OR Alarm_LowpH THEN
    SystemStatus := 'OUT OF COMPLIANCE';
ELSE
    SystemStatus := 'COMPLIANT - RUNNING';
END_IF

// ------------------------------------------------------------------
// 7. REGULATORY EMISSIONS LOGGING
//    Rolling log of pH/SOx/discharge state for MARPOL Annex VI
//    record-keeping. Overwrites oldest record once buffer is full -
//    in a real installation this streams to a non-volatile SCADA
//    historian rather than PLC-resident memory.
// ------------------------------------------------------------------
LogTimer(IN := System_Enable, PT := LogTimer_PT);
IF LogTimer.Q THEN
    LogTimer(IN := FALSE);   // retrigger next scan
    EmissionLog[LogIndex].Timestamp      := DT#2026-01-01-00:00:00; // replace with RTC read
    EmissionLog[LogIndex].pH_Value        := pH_Feedback;
    EmissionLog[LogIndex].SOx_ppm         := SOx_ppm;
    EmissionLog[LogIndex].DoseRate_Pct    := AlkalineDosingPump_Speed;
    EmissionLog[LogIndex].DischargeActive := WashWaterDischargeValve;
    EmissionLog[LogIndex].InECA           := GPS_InECA;

    LogIndex := LogIndex + 1;
    IF LogIndex > 999 THEN
        LogIndex := 0;
    END_IF
END_IF

END_FUNCTION_BLOCK
