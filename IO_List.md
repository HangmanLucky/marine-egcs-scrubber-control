# I/O List — Smart Exhaust Gas Cleaning System (EGCS)

**Project:** Automated Closed-Loop Scrubber Control
**Author:** Sipho Lucky Sibanda
**Target platform:** Siemens S7-1500 (TIA Portal / SCL) — portable to CODESYS-based marine PLCs

This list follows the format used on real Factory Acceptance Test (FAT) and commissioning
documentation for shipboard automation packages.

## Digital / Analogue Inputs

| Tag Name           | Description                                   | Signal Type    | Range / Units        | PLC Address (example) |
|---------------------|------------------------------------------------|-----------------|------------------------|--------------------------|
| `AI_pH_Feedback`     | Discharge water pH probe                        | 4–20 mA         | 0.00 – 14.00 pH        | `%IW100`                  |
| `AI_SOx_ppm`         | Exhaust gas SOx analyser                        | 4–20 mA         | 0 – 3000 ppm            | `%IW102`                  |
| `AI_ExhaustTemp`     | Exhaust gas temperature                         | Pt100 RTD       | 0 – 450 °C              | `%IW104`                  |
| `DI_GPS_InECA`       | Vessel-in-ECA flag from navigation/ECDIS system | Digital (24VDC) | 0 = Outside, 1 = Inside | `%IX10.0`                 |
| `DI_System_Enable`   | Master enable, bridge/ECR HMI                   | Digital (24VDC) | 0 = Off, 1 = Run        | `%IX10.1`                 |
| `DI_Sensor_Fault`    | Combined pH/SOx sensor comms fault relay        | Digital (24VDC) | 0 = OK, 1 = Fault       | `%IX10.2`                 |

## Digital / Analogue Outputs

| Tag Name                       | Description                              | Signal Type | Range / Units | PLC Address (example) |
|----------------------------------|--------------------------------------------|--------------|------------------|--------------------------|
| `AO_DosingPump_Speed`            | Alkaline (NaOH) dosing pump VFD reference  | 4–20 mA      | 0 – 100 %         | `%QW200`                  |
| `DO_WashWaterDischargeValve`     | Overboard discharge valve permissive       | Digital (24VDC) | 0 = Closed, 1 = Open | `%QX20.0`             |
| `DO_Alarm_HighSOx`               | High SOx alarm lamp/horn                   | Digital (24VDC) | —                | `%QX20.1`                  |
| `DO_Alarm_LowpH`                 | Low pH alarm lamp/horn                     | Digital (24VDC) | —                | `%QX20.2`                  |
| `DO_Alarm_ECA_Lockout`           | ECA lockout indicator (bridge + ECR panel) | Digital (24VDC) | —                | `%QX20.3`                  |
| `DO_Alarm_SensorFault`           | Sensor/comms fault indicator               | Digital (24VDC) | —                | `%QX20.4`                  |

## Notes for reviewers

- Addresses above are illustrative examples for a TIA Portal symbol table — a real
  commissioning I/O list would also include cabinet/terminal numbers, cable IDs, and
  loop-check sign-off columns.
- `DI_GPS_InECA` in a production system would come from an ECA-boundary lookup against
  live GPS position (e.g. a polygon check against IMO-published ECA charts) rather than
  a single hardwired bit — simplified here to a single flag for the PLC-side interlock.
- Setpoints (`pH_Setpoint`, `SOx_Limit_ppm`, etc.) are declared as internal `VAR` in
  `EGCS_ScrubberControl.st` and would normally be exposed as HMI-adjustable recipe
  values with password-level protection.
