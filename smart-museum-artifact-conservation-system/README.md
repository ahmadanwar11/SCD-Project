# Smart Museum Artifact Conservation System

## Task 1 — 12 Identified Operations

1. `powerOnSystem()` — Starts the chamber system.
2. `performSelfCheck()` — Checks sensors and control devices.
3. `registerArtifact()` — Records artifact information.
4. `loadEnvironmentProfile()` — Loads temperature and humidity limits.
5. `readSensors()` — Reads all important sensor values.
6. `startConservation()` — Starts normal conservation.
7. `correctTemperature()` — Corrects temperature.
8. `correctHumidity()` — Corrects humidity.
9. `activateProtection()` — Activates extra protection when correction fails.
10. `handleVibration()` — Responds to dangerous vibration.
11. `handleDoorOpen()` — Suspends conservation when the door opens.
12. `handlePowerFailure()` — Handles loss of power.

---

# Task 2 — Simple Operation Schemas

## 1. powerOnSystem()

**Purpose:** Start the chamber.

**Input:** Power supply.

**Output:** System started.

**Precondition:** Chamber has power.

**Postcondition:** Self-check starts.

---

## 2. performSelfCheck()

**Purpose:** Check essential sensors and control devices.

**Input:** Sensor and device status.

**Output:** PASS or FAIL.

**Precondition:** System is powered on.

**Postcondition:** If all checks pass, monitoring can begin.

**Failure:** Normal operation is blocked if an essential device fails.

---

## 3. registerArtifact()

**Purpose:** Record the artifact placed in the chamber.

**Input:** Artifact ID and information.

**Output:** Artifact record saved.

**Precondition:** System is working.

**Postcondition:** Artifact is registered for monitoring.

---

## 4. loadEnvironmentProfile()

**Purpose:** Load the artifact's required environmental limits.

**Input:** Temperature and humidity limits.

**Output:** Environmental profile loaded.

**Precondition:** Artifact is registered.

**Postcondition:** System can compare readings with the required limits.

---

## 5. readSensors()

**Purpose:** Read current chamber conditions.

**Input:** Sensor data.

**Output:** Temperature, humidity, light, vibration, door, artifact and power readings.

**Precondition:** Sensors are working.

**Postcondition:** Latest readings are available for checking.

---

## 6. startConservation()

**Purpose:** Start normal conservation.

**Input:** Door status, artifact profile and sensor readings.

**Output:** Conservation started.

**Precondition:** Self-check passed, artifact is registered, profile is loaded and door is closed.

**Postcondition:** System continuously monitors and controls the environment.

---

## 7. correctTemperature()

**Purpose:** Bring temperature back into the allowed range.

**Input:** Current temperature and allowed range.

**Output:** Temperature-control command.

**Precondition:** Temperature is outside the allowed range.

**Postcondition:** Sensor readings are checked again to confirm recovery.

**Failure:** If recovery takes too long, protection is activated.

---

## 8. correctHumidity()

**Purpose:** Bring humidity back into the allowed range.

**Input:** Current humidity and allowed range.

**Output:** Humidity-control command.

**Precondition:** Humidity is outside the allowed range.

**Postcondition:** Sensor readings are checked again to confirm recovery.

**Failure:** If recovery takes too long, protection is activated.

---

## 9. activateProtection()

**Purpose:** Protect the artifact when normal correction fails.

**Input:** Environmental failure information.

**Output:** Protection controls and operator alert.

**Precondition:** Temperature or humidity cannot be corrected in time.

**Postcondition:** Light may be reduced and extra controls may be activated.

---

## 10. handleVibration()

**Purpose:** Protect the artifact from significant vibration.

**Input:** Vibration reading.

**Output:** Risky activities suspended.

**Precondition:** Vibration is above the permitted threshold.

**Postcondition:** System waits until vibration stays below the threshold for the required stabilization time.

---

## 11. handleDoorOpen()

**Purpose:** Stop normal conservation when the door opens.

**Input:** Door sensor status.

**Output:** Conservation suspended.

**Precondition:** Door is open while an artifact is inside.

**Postcondition:** Conservation does not automatically restart after the door closes. Conditions must be checked first.

---

## 12. handlePowerFailure()

**Purpose:** Handle loss of power.

**Input:** Power status.

**Output:** Emergency power or safe shutdown.

**Precondition:** Main power is lost.

**Postcondition:** If emergency power is available, the system switches to it. Otherwise, the incident is recorded and the system safely shuts down.

---

## Simple Rules

- Self-check must pass before normal operation.
- The door must be closed for conservation.
- Temperature and humidity must stay within the artifact's limits.
- Corrections must be verified by sensor readings.
- Significant vibration suspends risky activities.
- Opening the door immediately suspends conservation.
- Power failure requires emergency power or safe shutdown.
- Artifact removal is allowed only when the chamber is confirmed safe.
