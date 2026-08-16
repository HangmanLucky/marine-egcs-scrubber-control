# Functional Test Procedure — EGCS Scrubber Control

**Project:** Smart Exhaust Gas Cleaning System (EGCS)
**Document type:** Factory Acceptance Test (FAT) — simulated / desktop validation
**Author:** Sipho Lucky Sibanda

This procedure verifies `FB_EGCS_ScrubberControl` behaves correctly across normal,
boundary, and fault conditions before it would be considered ready for a Site
Acceptance Test (SAT) on real I/O.

| # | Test Case | Precondition | Action | Expected Result | Pass/Fail |
|---|------------|----------------|---------|--------------------|-------------|
| 1 | System start-up | `System_Enable = FALSE` | Set `System_Enable = TRUE`, all sensors at nominal values | `SystemStatus` moves from `STANDBY` to `COMPLIANT - RUNNING`; dosing pump ramps from 0% | |
| 2 | pH closed-loop response | System running, `pH_Feedback = 7.0` | Step `pH_Feedback` down to `6.2` | `AlkalineDosingPump_Speed` increases smoothly (PID response, no oscillation > ±5%) | |
| 3 | pH low-low hard trip | System running | Force `pH_Feedback = 5.8` (below `pH_LowLow`) | `AlkalineDosingPump_Speed` snaps to 100%; `Alarm_LowpH = TRUE` | |
| 4 | High SOx alarm | System running, SOx nominal | Step `SOx_ppm` above `SOx_Limit_ppm` (11.5) | `Alarm_HighSOx = TRUE`; discharge valve permissive drops if SOx exceeds `SOx_HighHigh` | |
| 5 | ECA GPS interlock | System running, discharge active | Set `GPS_InECA = TRUE` | `WashWaterDischargeValve = FALSE` within one scan cycle; `Alarm_ECA_Lockout = TRUE`; `SystemStatus = "ECA - DISCHARGE LOCKED"` regardless of pH/SOx compliance | |
| 6 | ECA exit recovery | Continuing from Test 5 | Set `GPS_InECA = FALSE`, pH/SOx within limits | Discharge valve permissive returns to normal logic (no manual reset required) | |
| 7 | Sensor fault fail-safe | System running | Set `Sensor_Fault = TRUE` | Dosing pump forced to 0%, discharge valve forced closed, `SystemStatus = "SENSOR FAULT"` within one scan | |
| 8 | Fault recovery | Continuing from Test 7 | Clear `Sensor_Fault` | System resumes normal control without latching — confirm no false "bumped" pump output on recovery | |
| 9 | Emission logging cadence | System running for > 60s simulated | Observe `EmissionLog` array | New record written every 60s (`LogTimer`); `LogIndex` increments and wraps at 999→0 | |
| 10 | Manual disable | System running | Set `System_Enable = FALSE` | Dosing pump ramps to 0%, discharge valve closes, `SystemStatus = "STANDBY"` | |

## How to exercise these tests without physical I/O

For a portfolio/simulation build (no real S7-1500 hardware), these test cases can be
run against:

- **TIA Portal PLCSIM** — force input tags directly in the watch table and observe
  outputs, or
- **A companion Python/soft-PLC harness** — feed synthetic sensor values into the
  same input structure and log outputs, useful for producing the trend screenshots
  used in the HMI/README.

## Sign-off

| Role | Name | Date |
|------|------|------|
| Test performed by | Sipho Lucky Sibanda | |
| Reviewed by | | |
