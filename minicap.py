from subprocess import check_output, call




abi = check_output("adb -s $id shell getprop ro.product.cpu.abi | tr -d '\r'".split())
sdk = check_output("adb -s $id shell getprop ro.build.version.sdk | tr -d '\r'".split())
pre = check_output("adb -s $id shell getprop ro.build.version.preview_sdk | tr -d '\r'".split())
rel = check_output("adb -s $id shell getprop ro.build.version.release | tr -d '\r'".split())


dir = "/data/local/tmp/minicap-devel"

call("adb -s $id shell mkdir $dir 2>/dev/null || true".split())
