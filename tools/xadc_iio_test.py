from pathlib import Path

print("=== XADC / IIO automatic test ===\n")

iio_root = Path("/sys/bus/iio/devices")
devices = sorted(iio_root.glob("iio:device*"))

if not devices:
    print("FAIL: No IIO devices found.")
else:
    print(f"Found {len(devices)} IIO device(s).\n")

    xadc_found = False

    for dev in devices:
        name_file = dev / "name"
        name = name_file.read_text().strip() if name_file.exists() else "unknown"

        print(f"Device: {dev}")
        print(f"Name:   {name}")

        temp_raw_files = sorted(dev.glob("in_temp*_raw"))

        if temp_raw_files:
            xadc_found = True

            for raw_file in temp_raw_files:
                prefix = raw_file.name[:-4]   # remove "_raw"

                scale_file = dev / f"{prefix}_scale"
                offset_file = dev / f"{prefix}_offset"

                raw = float(raw_file.read_text().strip())

                print(f"\n  {raw_file.name} = {raw}")

                if scale_file.exists():
                    scale = float(scale_file.read_text().strip())
                    print(f"  {scale_file.name} = {scale}")
                else:
                    scale = None
                    print("  scale not found")

                if offset_file.exists():
                    offset = float(offset_file.read_text().strip())
                    print(f"  {offset_file.name} = {offset}")
                else:
                    offset = 0
                    print("  offset not found")

                if scale is not None:
                    value = (raw + offset) * scale
                    print(f"  Calculated value = {value}")

                    if abs(value) > 1000:
                        print(f"  Temperature ≈ {value / 1000:.2f} °C")
                    else:
                        print(f"  Temperature ≈ {value:.2f} °C")

        voltage_files = sorted(dev.glob("in_voltage*_raw"))
        if voltage_files:
            print("\n  Voltage channels:")
            for f in voltage_files:
                print("   ", f.name)

        print()

    if xadc_found:
        print("RESULT: Temperature channel detected.")
        print("XADC can probably be used for Lab 3.")
    else:
        print("RESULT: IIO exists, but no temperature channel was detected.")
