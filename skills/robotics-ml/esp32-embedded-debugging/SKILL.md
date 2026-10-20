---
name: esp32-embedded-debugging
description: "Debug ESP32 firmware and hardware: serial monitor output, boot loops and brownouts, watchdog resets, backtrace decoding, flashing failures, and serial communication with sensors or motor drivers. Use when an ESP32 resets, hangs, prints garbage, fails to flash, or talks to peripherals incorrectly."
---

# ESP32 Embedded Debugging

Separate the three layers before changing code: **power and boot** (does the chip run stably?), **serial link** (can the host see clean output?), and **firmware logic** (does the code do what you intended?). Most field failures are in the first two.

## Step 1: Find the device and the right tool

```bash
ls /dev/ttyUSB* /dev/ttyACM* 2>/dev/null   # USB-serial adapters and dev boards
dmesg | tail -20                            # shows which device node the board enumerated as
```

- Use `idf.py monitor` for ESP-IDF projects, or `pio device monitor` for PlatformIO. Both decode backtraces; a raw terminal does not.
- If the device exists but opening it fails with permission denied, the user must add their account to the `dialout` group themselves. Do not change system groups or use `sudo` from an agent session.
- Check the chip before debugging firmware:
  ```bash
  esptool.py chip_id          # confirms the chip is reachable and identifies its variant
  ```

## Step 2: Read the boot log, not just the last line

Reset the board and capture the full output from the first byte:

- `rst:0x1 (POWERON)` means a cold start. Repeated `rst:0xc (SW_CPU_RESET)`, `rst:0x10 (RTCWDT_RTC_RESET)`, or `Brownout detector was triggered` means something other than the code is resetting the chip.
- `Brownout detector was triggered` points at supply: a USB port that cannot source enough current, a long or thin cable, or a motor or servo sharing the 3.3 V rail. Measure the 3.3 V line under load before changing firmware.
- `Guru Meditation Error` followed by a `Backtrace:` line is a crash. Decode it with `idf.py monitor` or `xtensa-esp32-elf-addr2line -pfiaC -e build/<app>.elf <addresses>`.
- Watchdog resets (`Task watchdog got triggered`) mean a task starved the CPU. Look for busy loops without `vTaskDelay` or `yield`, and for blocking calls inside ISRs.

## Step 3: Check the serial link

Garbled output is usually a configuration problem, not a firmware bug:

- Baud rate must match on both sides. The ROM bootloader prints at 115200 regardless of the application's setting, so a clean boot log followed by garbage means the application changed the baud rate.
- Confirm the TX/RX lines are not swapped. Symptom: nothing printed, or a single byte of noise.
- Keep the USB-serial adapter's logic level at 3.3 V. Never connect 5 V TTL to an ESP32 GPIO.
- For sensors and motor drivers over UART, log raw bytes in hex on both ends before parsing. Framing errors show up as bytes that are valid but misaligned.

## Step 4: Flashing failures

- `Failed to connect to ESP32: Timed out waiting for packet header` usually means the chip is not in download mode. Hold BOOT (GPIO0 low) during reset, or use the board's auto-reset circuit.
- Keep the flashing baud rate modest (for example 460800 or 115200) when cables are long.
- A flash that succeeds but then boot-loops often comes from a partition table or flash-size mismatch. Check the `flash_size` in the board configuration against the physical part.

## Step 5: Isolate firmware logic

1. Reduce to a minimal sketch that prints a heartbeat every second with the free heap (`esp_get_free_heap_size()`).
2. Add one peripheral at a time and re-check the boot log after each step.
3. For intermittent faults, log with timestamps and sequence numbers so you can correlate a reset with the last successful operation.

## Hardware checks worth doing before blaming code

- Shared grounds between the ESP32, sensor, and motor driver.
- Decoupling capacitors near the module's supply pins.
- Strapping pins (GPIO0, GPIO2, GPIO12, and others) pulled to the wrong level at boot by external circuitry.
- Motor back-EMF or inductive spikes coupling into the supply during PWM changes.

## Reporting

State the observed symptom from the first boot-log line, the layer where you found the cause (power, serial, or logic), the evidence (exact log lines or measurements), and what was changed. If you could not measure the supply or reproduce on the real hardware, say so.
