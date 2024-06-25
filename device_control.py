
import subprocess

def run_command(command):
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, text=True)
    return result.stdout.strip()

def get_all_bdfs():
    # Run lspci to get all BDFs
    pci_output = run_command("lspci")
    bdfs = []
    for line in pci_output.split('\n'):
        if line:
            bdf = line.split(' ')[0]
            bdfs.append(bdf)
    return bdfs

def modify_hex_last_digit(hex_str):
    return hex_str[:-1] + '0'

# Dictionary to store original values
original_values = {}

def store_original_values(bdfs):
    for bdf in bdfs:
        try:
            command = f"setpci -s {bdf} CAP_EXP+0x08.w"
            output = run_command(command)
            if output:
                original_values[bdf] = output
        except Exception as e:
            print(f"Error storing original value for BDF {bdf}: {str(e)}")

def reset_to_original_values():
    for bdf, original_value in original_values.items():
        try:
            set_command = f"sudo setpci -s {bdf} CAP_EXP+0x08.w={original_value}"
            run_command(set_command)
            print(f"BDF: {bdf}, Reset to Original: {original_value}")
        except Exception as e:
            print(f"Error resetting value for BDF {bdf}: {str(e)}")

def process_bdfs(bdfs):
    for bdf in bdfs:
        try:
            command = f"setpci -s {bdf} CAP_EXP+0x08.w"
            output = run_command(command)
            if output:
                modified = modify_hex_last_digit(output)
                set_command = f"sudo setpci -s {bdf} CAP_EXP+0x08.w={modified}"
                run_command(set_command)
                print(f"BDF: {bdf}, Original: {output}, Modified: {modified}")
        except Exception as e:
            print(f"Error processing BDF {bdf}: {str(e)}")

# Example usage
if __name__ == "__main__":
    bdfs = get_all_bdfs()
    store_original_values(bdfs)
    process_bdfs(bdfs)
    # Assume some operations from sbr are performed here
    reset_to_original_values()
