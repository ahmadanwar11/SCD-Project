# Smart Museum Artifact Conservation System

## Task 1 — Identified Operations

The following operations are derived directly from the scenario. State names such as `MONITORING`, `CONSERVATION_ACTIVE`, `PROTECTION_MODE`, and `VIBRATION_RESPONSE` are not used as operation names.

| # | Operation | Purpose |
|---|---|---|
| 1 | `powerOnChamber()` | Starts the conservation chamber and initiates system startup. |
| 2 | `performSelfCheck()` | Verifies that all essential sensors and environmental-control devices are functioning. |
| 3 | `recordArtifact()` | Records the artifact identification information when an artifact is placed inside. |
| 4 | `loadEnvironmentalProfile()` | Loads the temperature, humidity, and other required limits for the artifact. |
| 5 | `readSensorData()` | Collects the current readings from temperature, humidity, light, vibration, door, artifact-condition, and power sensors. |
| 6 | `verifyDoorClosed()` | Determines whether the chamber door is closed and suitable for active conservation. |
| 7 | `startConservation()` | Begins normal environmental-control activity after required conditions are satisfied. |
| 8 | `checkEnvironmentalLimits()` | Compares actual temperature and humidity against the artifact's permitted ranges. |
| 9 | `correctTemperature()` | Commands the environmental-control mechanism to restore temperature to the permitted range. |
| 10 | `correctHumidity()` | Commands the environmental-control mechanism to restore humidity to the permitted range. |
| 11 | `verifyEnvironmentalRecovery()` | Confirms through fresh sensor readings that a corrected environmental condition has actually returned to its permitted range. |
| 12 | `handleRecoveryTimeout()` | Handles a temperature or humidity condition that could not be corrected within the allowed recovery period. |
| 13 | `activateProtectionControls()` | Reduces light exposure and/or activates additional environmental controls to protect the artifact. |
| 14 | `generateOperatorAlert()` | Sends/records an alert for the museum operator when protection is required. |
| 15 | `detectVibration()` | Detects vibration above the permitted threshold while an artifact is present. |
| 16 | `suspendRiskIncreasingActivities()` | Temporarily stops activities that could increase risk to the artifact during significant vibration. |
| 17 | `verifyVibrationStabilization()` | Confirms that vibration has remained below the permitted threshold for the required stabilization period. |
| 18 | `handleDoorOpened()` | Immediately suspends normal conservation activities when the chamber door is opened. |
| 19 | `verifyResumeConditions()` | After the door is closed, verifies environmental conditions and sensor health before resuming conservation. |
| 20 | `handlePowerFailure()` | Detects power loss and initiates emergency-power handling. |
| 21 | `switchToEmergencyPower()` | Transfers operation to the emergency power source when available. |
| 22 | `recordPowerIncident()` | Records the power-loss incident when emergency power is unavailable. |
| 23 | `performSafeShutdown()` | Places the chamber into a safe shutdown condition when continued operation is not possible. |
| 24 | `verifySafeRemovalConditions()` | Confirms that the chamber is safe and no protection response is active before artifact removal. |
| 25 | `removeArtifact()` | Authorizes and records removal of the artifact after safe-removal conditions are verified. |

---

# Task 2 — Complete Operation Schema

## Operation 1 — powerOnChamber

**Operation:** `powerOnChamber()`

**Purpose:** Start the chamber and prepare it for operation.

**Inputs:** None.

**Outputs:** Startup initiated; self-check requested.

**Preconditions:**
- Chamber is connected to a power source.
- System is not already running.

**Postconditions:**
- Chamber power is marked available.
- Startup sequence is initiated.
- `performSelfCheck()` is invoked.

**Failure/Exception Conditions:**
- If power is unavailable, startup cannot proceed.
- If startup hardware is unavailable, the system records the failure.

**Related Operations:** `performSelfCheck()`, `handlePowerFailure()`

---

## Operation 2 — performSelfCheck

**Operation:** `performSelfCheck()`

**Purpose:** Verify all essential sensors and environmental-control devices before normal monitoring is permitted.

**Inputs:** Current sensor/device status.

**Outputs:** Self-check result: PASS or FAIL.

**Preconditions:**
- Chamber startup has been initiated.

**Postconditions on PASS:**
- All essential sensors are confirmed operational.
- Environmental-control devices are confirmed operational.
- System is permitted to begin monitoring.

**Postconditions on FAIL:**
- Normal conservation operation is blocked.
- Fault information is recorded.
- Operator notification may be generated.

**Failure/Exception Conditions:**
- Any essential sensor failure.
- Any essential environmental-control device failure.

**Related Operations:** `powerOnChamber()`, `readSensorData()`

---

## Operation 3 — recordArtifact

**Operation:** `recordArtifact(artifactId, identificationData)`

**Purpose:** Register the artifact placed inside the chamber.

**Inputs:**
- `artifactId`
- Artifact identification information.

**Outputs:** Artifact record created/updated.

**Preconditions:**
- Chamber is operational.
- Artifact is physically detected/placed inside.
- Self-check has succeeded.

**Postconditions:**
- Artifact identification information is stored.
- Artifact is associated with the current chamber session.
- Monitoring of the artifact can begin.

**Failure/Exception Conditions:**
- Missing or invalid artifact identification data.
- Artifact cannot be detected/confirmed.

**Related Operations:** `loadEnvironmentalProfile()`, `readSensorData()`

---

## Operation 4 — loadEnvironmentalProfile

**Operation:** `loadEnvironmentalProfile(artifactId, profile)`

**Purpose:** Load the environmental requirements for the artifact.

**Inputs:**
- `artifactId`
- Environmental profile containing permitted temperature and humidity ranges.
- Other applicable limits such as vibration/light thresholds when defined.

**Outputs:** Environmental profile loaded.

**Preconditions:**
- Artifact has been recorded.
- A valid environmental profile exists.

**Postconditions:**
- Required environmental limits are stored as the active profile.
- The system can compare actual readings against artifact-specific limits.

**Failure/Exception Conditions:**
- Profile missing.
- Profile incomplete.
- Profile contains invalid limits.

**Related Operations:** `recordArtifact()`, `checkEnvironmentalLimits()`

---

## Operation 5 — readSensorData

**Operation:** `readSensorData()`

**Purpose:** Obtain the current condition of the chamber and artifact environment.

**Inputs:** Sensor interfaces.

**Outputs:**
- Temperature reading.
- Humidity reading.
- Light exposure reading.
- Vibration reading.
- Door status.
- Artifact-condition reading.
- Power availability.
- Sensor health/status.

**Preconditions:**
- System has power or an available emergency power source.

**Postconditions:**
- Latest readings are available to the monitoring logic.
- Sensor health information is updated.

**Failure/Exception Conditions:**
- Sensor unavailable.
- Sensor returns invalid/unreadable data.

**Related Operations:** `performSelfCheck()`, `checkEnvironmentalLimits()`, `verifyEnvironmentalRecovery()`, `verifyResumeConditions()`

---

## Operation 6 — verifyDoorClosed

**Operation:** `verifyDoorClosed()`

**Purpose:** Determine whether active conservation is allowed based on chamber door status.

**Inputs:** Door sensor status.

**Outputs:** Boolean result: closed/open.

**Preconditions:**
- Door sensor is operational.

**Postconditions:**
- Current door condition is recorded.
- Active conservation is permitted only when the door is confirmed closed.

**Failure/Exception Conditions:**
- Door sensor failure or indeterminate reading.

**Related Operations:** `startConservation()`, `handleDoorOpened()`, `verifyResumeConditions()`

---

## Operation 7 — startConservation

**Operation:** `startConservation()`

**Purpose:** Start normal artifact conservation.

**Inputs:** Door status, artifact profile, sensor status, current environmental readings.

**Outputs:** Normal conservation activities activated.

**Preconditions:**
- Self-check succeeded.
- Artifact is recorded.
- Environmental profile is loaded.
- Door is confirmed closed.
- Essential sensors are operational.
- No active protection or vibration response is underway.

**Postconditions:**
- Normal environmental-control process is activated.
- Continuous environmental monitoring begins.

**Failure/Exception Conditions:**
- Door open.
- Missing artifact profile.
- Sensor fault.
- Active protection/vibration response.

**Related Operations:** `verifyDoorClosed()`, `loadEnvironmentalProfile()`, `verifyResumeConditions()`

---

## Operation 8 — checkEnvironmentalLimits

**Operation:** `checkEnvironmentalLimits(temperature, humidity, profile)`

**Purpose:** Determine whether temperature and humidity satisfy the artifact's required limits.

**Inputs:**
- Current temperature.
- Current humidity.
- Artifact environmental profile.

**Outputs:**
- Temperature status: within/outside range.
- Humidity status: within/outside range.

**Preconditions:**
- Artifact environmental profile is loaded.
- Valid sensor readings are available.

**Postconditions:**
- Environmental status is classified.
- A correction operation is requested when a limit is exceeded.

**Failure/Exception Conditions:**
- Invalid sensor reading.
- Missing environmental profile.

**Related Operations:** `readSensorData()`, `correctTemperature()`, `correctHumidity()`

---

## Operation 9 — correctTemperature

**Operation:** `correctTemperature(targetRange)`

**Purpose:** Attempt to restore temperature to the artifact's permitted range.

**Inputs:** Permitted temperature range.

**Outputs:** Temperature-control command issued.

**Preconditions:**
- Temperature is outside the permitted range.
- Temperature-control mechanism is operational.
- Chamber is in a condition where environmental control may safely operate.

**Postconditions:**
- Corrective temperature control is activated.
- Recovery monitoring begins.
- The system does not mark the condition safe until sensor verification succeeds.

**Failure/Exception Conditions:**
- Control mechanism unavailable.
- Temperature cannot be corrected within the recovery period.

**Related Operations:** `checkEnvironmentalLimits()`, `verifyEnvironmentalRecovery()`, `handleRecoveryTimeout()`

---

## Operation 10 — correctHumidity

**Operation:** `correctHumidity(targetRange)`

**Purpose:** Attempt to restore humidity to the artifact's permitted range.

**Inputs:** Permitted humidity range.

**Outputs:** Humidity-control command issued.

**Preconditions:**
- Humidity is outside the permitted range.
- Humidity-control mechanism is operational.

**Postconditions:**
- Corrective humidity control is activated.
- Recovery monitoring begins.
- Safety is confirmed only after sensor verification.

**Failure/Exception Conditions:**
- Control mechanism unavailable.
- Humidity cannot be corrected within the recovery period.

**Related Operations:** `checkEnvironmentalLimits()`, `verifyEnvironmentalRecovery()`, `handleRecoveryTimeout()`

---

## Operation 11 — verifyEnvironmentalRecovery

**Operation:** `verifyEnvironmentalRecovery(conditionType, permittedRange)`

**Purpose:** Verify that an environmental correction actually succeeded.

**Inputs:**
- Condition type: temperature or humidity.
- Permitted range.
- Fresh sensor readings.
- Recovery timer/status.

**Outputs:** Recovery result: VERIFIED or NOT_VERIFIED.

**Preconditions:**
- A corrective command has previously been issued.
- Relevant sensor is operational.

**Postconditions on VERIFIED:**
- Environmental condition is confirmed within the permitted range.
- Normal monitoring may continue.

**Postconditions on NOT_VERIFIED:**
- Recovery remains active, or timeout handling is initiated if the allowed period has expired.

**Failure/Exception Conditions:**
- Sensor failure.
- Recovery timeout.

**Important Rule:** Issuing a correction command alone does not make the artifact safe. Fresh sensor readings must confirm recovery.

**Related Operations:** `correctTemperature()`, `correctHumidity()`, `handleRecoveryTimeout()`

---

## Operation 12 — handleRecoveryTimeout

**Operation:** `handleRecoveryTimeout(conditionType)`

**Purpose:** Respond when an environmental condition cannot be corrected within the allowed recovery period.

**Inputs:** Failed condition type and recovery status.

**Outputs:** Protection response initiated.

**Preconditions:**
- Temperature or humidity remains outside its permitted range.
- Allowed recovery period has expired.

**Postconditions:**
- Normal conservation is suspended.
- Protection controls are activated.
- Operator alert is generated.

**Failure/Exception Conditions:**
- Protection control unavailable; incident is recorded and additional safe-response procedures are initiated.

**Related Operations:** `verifyEnvironmentalRecovery()`, `activateProtectionControls()`, `generateOperatorAlert()`

---

## Operation 13 — activateProtectionControls

**Operation:** `activateProtectionControls()`

**Purpose:** Prioritize artifact protection when normal environmental recovery fails.

**Inputs:** Current environmental condition and artifact profile.

**Outputs:** Protection controls activated.

**Preconditions:**
- A serious environmental condition cannot be corrected within the allowed recovery period.

**Postconditions:**
- Light exposure may be reduced.
- Additional environmental controls may be activated.
- Normal conservation remains suspended until safe recovery is established.

**Failure/Exception Conditions:**
- Required protection mechanism unavailable.

**Related Operations:** `handleRecoveryTimeout()`, `generateOperatorAlert()`

---

## Operation 14 — generateOperatorAlert

**Operation:** `generateOperatorAlert(alertType, details)`

**Purpose:** Notify the museum operator about a condition requiring attention.

**Inputs:**
- Alert type.
- Environmental/sensor details.
- Artifact identifier.
- Time of incident.

**Outputs:** Alert generated and recorded.

**Preconditions:**
- A condition requiring operator attention has been detected.

**Postconditions:**
- Alert is stored and/or delivered to the operator.
- Incident information is available for later review.

**Failure/Exception Conditions:**
- Notification mechanism unavailable; alert is retained locally if possible.

**Related Operations:** `handleRecoveryTimeout()`, `handlePowerFailure()`, `detectVibration()`

---

## Operation 15 — detectVibration

**Operation:** `detectVibration(vibrationReading, threshold)`

**Purpose:** Detect significant vibration that may endanger the artifact.

**Inputs:**
- Current vibration reading.
- Permitted vibration threshold.

**Outputs:** Vibration status: NORMAL or SIGNIFICANT.

**Preconditions:**
- Artifact is inside the chamber.
- Vibration sensor is operational.

**Postconditions when significant vibration is detected:**
- Vibration response is initiated.
- Activities that could increase risk are suspended.

**Failure/Exception Conditions:**
- Vibration sensor failure or invalid reading.

**Related Operations:** `suspendRiskIncreasingActivities()`, `verifyVibrationStabilization()`

---

## Operation 16 — suspendRiskIncreasingActivities

**Operation:** `suspendRiskIncreasingActivities()`

**Purpose:** Temporarily stop activities that could increase artifact risk during significant vibration.

**Inputs:** Vibration-response condition.

**Outputs:** Risk-increasing activities suspended.

**Preconditions:**
- Significant vibration has been detected.

**Postconditions:**
- Potentially harmful active processes are suspended.
- Vibration stabilization monitoring begins.

**Failure/Exception Conditions:**
- A controllable activity cannot be suspended; incident is recorded and operator is alerted.

**Related Operations:** `detectVibration()`, `verifyVibrationStabilization()`

---

## Operation 17 — verifyVibrationStabilization

**Operation:** `verifyVibrationStabilization(threshold, stabilizationPeriod)`

**Purpose:** Confirm that vibration has remained safely below the permitted threshold for the required period.

**Inputs:**
- Vibration threshold.
- Required stabilization period.
- Continuous vibration readings.

**Outputs:** Stabilization result: VERIFIED or NOT_VERIFIED.

**Preconditions:**
- Vibration response is active.
- Vibration sensor is operational.

**Postconditions on VERIFIED:**
- Vibration has remained below the threshold for the complete stabilization period.
- Resume checks may begin.

**Postconditions on NOT_VERIFIED:**
- Vibration response continues or restarts.

**Important Rule:** A single reading below the threshold is insufficient; the threshold must remain satisfied for the required stabilization period.

**Related Operations:** `detectVibration()`, `suspendRiskIncreasingActivities()`, `verifyResumeConditions()`

---

## Operation 18 — handleDoorOpened

**Operation:** `handleDoorOpened()`

**Purpose:** Immediately suspend normal conservation when the chamber door is opened.

**Inputs:** Door sensor event.

**Outputs:** Normal conservation suspended.

**Preconditions:**
- Artifact is inside the chamber.
- Door sensor reports OPEN.

**Postconditions:**
- Normal conservation activities are immediately suspended.
- The system continues monitoring relevant conditions.
- Conservation is not automatically resumed when the door closes.

**Failure/Exception Conditions:**
- Door sensor failure; condition is treated as unsafe/indeterminate.

**Related Operations:** `verifyDoorClosed()`, `verifyResumeConditions()`

---

## Operation 19 — verifyResumeConditions

**Operation:** `verifyResumeConditions()`

**Purpose:** Verify that conservation can safely resume after an interruption such as an open door.

**Inputs:**
- Door status.
- Current environmental readings.
- Sensor health.
- Artifact profile.
- Protection/vibration status.

**Outputs:** Resume decision: ALLOWED or BLOCKED.

**Preconditions:**
- Door has been closed after being open, or another interruption has ended.

**Postconditions on ALLOWED:**
- Required sensor status is healthy.
- Environmental conditions are verified.
- No active protection response prevents resumption.
- Normal conservation may resume.

**Postconditions on BLOCKED:**
- Normal conservation remains suspended.
- Appropriate corrective/protection operation continues.

**Failure/Exception Conditions:**
- Door not closed.
- Environmental conditions outside limits.
- Sensor failure.
- Active vibration/protection response.

**Related Operations:** `verifyDoorClosed()`, `readSensorData()`, `verifyEnvironmentalRecovery()`, `verifyVibrationStabilization()`, `startConservation()`

---

## Operation 20 — handlePowerFailure

**Operation:** `handlePowerFailure()`

**Purpose:** Respond to loss of primary power during conservation.

**Inputs:** Power availability status.

**Outputs:** Emergency-power transfer or safe-shutdown initiation.

**Preconditions:**
- Chamber is operating.
- Power sensor detects loss of primary power.

**Postconditions when emergency power is available:**
- Emergency power is activated.
- Critical monitoring/protection functions continue.

**Postconditions when emergency power is unavailable:**
- Incident is recorded.
- Safe shutdown is initiated.

**Failure/Exception Conditions:**
- Emergency power unavailable.
- Emergency transfer fails.

**Related Operations:** `switchToEmergencyPower()`, `recordPowerIncident()`, `performSafeShutdown()`

---

## Operation 21 — switchToEmergencyPower

**Operation:** `switchToEmergencyPower()`

**Purpose:** Transfer chamber operation to an available emergency power source.

**Inputs:** Emergency power availability/status.

**Outputs:** Emergency power activated.

**Preconditions:**
- Primary power has failed.
- Emergency power source is available.

**Postconditions:**
- Emergency power supplies the required system functions.
- Critical monitoring and protection continue.

**Failure/Exception Conditions:**
- Emergency power transfer fails.

**Related Operations:** `handlePowerFailure()`

---

## Operation 22 — recordPowerIncident

**Operation:** `recordPowerIncident(details)`

**Purpose:** Create an incident record when power is lost and emergency power cannot be used.

**Inputs:**
- Time of failure.
- Power status.
- Current artifact/chamber condition.
- Relevant sensor readings.

**Outputs:** Power incident recorded.

**Preconditions:**
- Primary power has failed.
- Emergency power is unavailable or failed.

**Postconditions:**
- Incident is permanently/logically recorded.
- Safe shutdown can proceed.

**Failure/Exception Conditions:**
- Logging storage unavailable; system attempts the safest available fallback.

**Related Operations:** `handlePowerFailure()`, `performSafeShutdown()`

---

## Operation 23 — performSafeShutdown

**Operation:** `performSafeShutdown()`

**Purpose:** Place the chamber in a safe state when continued operation is impossible.

**Inputs:** Current chamber, artifact, power, and protection status.

**Outputs:** Safe shutdown completed.

**Preconditions:**
- Continued normal operation is impossible or unsafe.
- Primary and emergency power are unavailable, or another critical failure requires shutdown.

**Postconditions:**
- Non-essential activities are stopped.
- Artifact-protection measures that remain possible are maintained.
- Chamber is marked as safely shut down.
- Further artifact removal is blocked until safety is established.

**Failure/Exception Conditions:**
- A shutdown actuator fails; failure is recorded and remaining protective actions continue.

**Related Operations:** `recordPowerIncident()`, `handlePowerFailure()`, `verifySafeRemovalConditions()`

---

## Operation 24 — verifySafeRemovalConditions

**Operation:** `verifySafeRemovalConditions()`

**Purpose:** Determine whether an operator is permitted to remove the artifact.

**Inputs:**
- Chamber condition.
- Environmental readings.
- Door status.
- Sensor status.
- Protection-response status.
- Artifact status.

**Outputs:** Removal authorization: ALLOWED or DENIED.

**Preconditions:**
- An artifact is present.
- Operator has requested removal.

**Postconditions on ALLOWED:**
- Chamber is confirmed safe for artifact removal.
- No active protection response is underway.
- Removal is authorized.

**Postconditions on DENIED:**
- Artifact remains in the chamber.
- The active protection/correction response continues.

**Failure/Exception Conditions:**
- Any safety condition cannot be verified.

**Related Operations:** `readSensorData()`, `verifyEnvironmentalRecovery()`, `verifyVibrationStabilization()`, `removeArtifact()`

---

## Operation 25 — removeArtifact

**Operation:** `removeArtifact(artifactId)`

**Purpose:** Remove an artifact only after the system confirms safe conditions.

**Inputs:** Artifact identifier and removal authorization.

**Outputs:** Artifact record updated; artifact removed from active chamber monitoring.

**Preconditions:**
- Artifact exists in the chamber.
- `verifySafeRemovalConditions()` has returned ALLOWED.
- No active protection response is underway.

**Postconditions:**
- Artifact is removed from the active chamber session.
- Artifact monitoring for the current session ends.
- Artifact record is retained for historical/audit purposes.

**Failure/Exception Conditions:**
- Safety authorization denied.
- Artifact identifier does not match the active artifact.

**Related Operations:** `verifySafeRemovalConditions()`, `recordArtifact()`

---

# Overall System Rules

1. **Self-check is mandatory.** Normal monitoring/conservation cannot begin until all essential sensors and environmental-control devices pass the self-check.
2. **Door-open safety rule.** Normal conservation must be suspended immediately whenever the chamber door is opened.
3. **No automatic resume after door closure.** Closing the door only permits resume verification; it does not itself restart conservation.
4. **Correction requires verification.** A control command is not proof that the environment has recovered. Fresh sensor readings must confirm the required range.
5. **Recovery timeout causes protection.** If temperature or humidity cannot be corrected within the allowed recovery period, normal conservation stops and protection controls are activated.
6. **Vibration requires stabilization.** The system must verify that vibration remains below the permitted threshold for the complete stabilization period before normal conservation can resume.
7. **Power failure requires contingency handling.** Emergency power is used when available; otherwise the incident is recorded and the system enters safe shutdown.
8. **Safe artifact removal is conditional.** The operator may remove an artifact only after the system confirms safe chamber conditions and confirms that no active protection response is underway.
9. **Continuous monitoring.** Temperature, humidity, light, vibration, door status, artifact condition, and power availability are monitored throughout operation.
10. **Artifact-specific limits.** Environmental decisions are based on the loaded artifact profile rather than generic room-comfort settings.

# Compact Operation Relationship Flow

```text
powerOnChamber
      |
      v
performSelfCheck
      |
      +---- FAIL ----> block normal operation / alert
      |
     PASS
      |
      v
recordArtifact
      |
      v
loadEnvironmentalProfile
      |
      v
verifyDoorClosed
      |
      +---- OPEN ----> continue monitoring
      |
    CLOSED
      |
      v
startConservation
      |
      v
readSensorData
      |
      +---- temperature outside ----> correctTemperature
      |                                  |
      |                                  v
      |                        verifyEnvironmentalRecovery
      |                                  |
      |                            timeout / fail
      |                                  |
      |                                  v
      |                        handleRecoveryTimeout
      |                                  |
      |                                  v
      |                        activateProtectionControls
      |
      +---- humidity outside -----> correctHumidity
      |                                  |
      |                                  v
      |                        verifyEnvironmentalRecovery
      |
      +---- significant vibration -> suspendRiskIncreasingActivities
      |                                  |
      |                                  v
      |                        verifyVibrationStabilization
      |
      +---- door opened ----------> handleDoorOpened
      |                                  |
      |                             door closed
      |                                  v
      |                        verifyResumeConditions
      |
      +---- power lost ----------> handlePowerFailure
                                         |
                              +----------+----------+
                              |                     |
                         emergency power       unavailable
                              |                     |
                              v                     v
                     switchToEmergencyPower  recordPowerIncident
                                                    |
                                                    v
                                           performSafeShutdown

Operator requests removal
      |
      v
verifySafeRemovalConditions
      |
   ALLOWED
      |
      v
removeArtifact
```

# Traceability Matrix

| Requirement from Scenario | Operation(s) |
|---|---|
| Power-on and self-check | `powerOnChamber()`, `performSelfCheck()` |
| Block normal operation if essential checks fail | `performSelfCheck()` |
| Record artifact identification | `recordArtifact()` |
| Load artifact environmental limits | `loadEnvironmentalProfile()` |
| Door must be closed for active conservation | `verifyDoorClosed()`, `startConservation()` |
| Continuous monitoring | `readSensorData()` |
| Compare temperature/humidity with limits | `checkEnvironmentalLimits()` |
| Correct temperature | `correctTemperature()` |
| Correct humidity | `correctHumidity()` |
| Verify correction through sensors | `verifyEnvironmentalRecovery()` |
| Recovery timeout | `handleRecoveryTimeout()` |
| Enter protective response | `activateProtectionControls()` |
| Alert operator | `generateOperatorAlert()` |
| Detect vibration | `detectVibration()` |
| Suspend risky activities | `suspendRiskIncreasingActivities()` |
| Verify vibration stabilization | `verifyVibrationStabilization()` |
| Suspend when door opens | `handleDoorOpened()` |
| Verify conditions before resuming | `verifyResumeConditions()` |
| Emergency power | `handlePowerFailure()`, `switchToEmergencyPower()` |
| Record power incident | `recordPowerIncident()` |
| Safe shutdown | `performSafeShutdown()` |
| Safe artifact removal | `verifySafeRemovalConditions()`, `removeArtifact()` |

# Submission Notes

- Task 1 requires at least 12 operations; this solution identifies **25 operations**.
- No state name is used as an operation name.
- Each operation includes purpose, inputs, outputs, preconditions, postconditions, failure/exception conditions, and related operations where applicable.
- Safety-critical rules from the scenario are explicitly represented in the schemas.
