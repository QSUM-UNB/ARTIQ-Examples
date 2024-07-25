# ARTIQ-Examples

Example code for ARTIQ (Advanced Real-Time Infrastructure for Quantum physics) hardware systems.

## Example files
Below is the list of example files we wrote to test different ARTIQ devices:

1) `Sampler_Fast.py`
2) `Sampler_Fast_Trigger.py`
3) `Sampler_SaveToFile.py`
4) `TTL_SingleRead.py`
5) `TTL_Trigger.py`
6) `TTL_led_sos.py`
7) `TTL_rtio.py`
8) `Urukul_Test.py`
9) `Zotino_Test.py`
10) `Zotino_Wave.py`

## Other Resources
- Manual: https://m-labs.hk/artiq/manual/
- Forum: https://forum.m-labs.hk/
- Device Datasheets: https://m-labs.hk/experiment-control/sinara-core/
- ARTIQ GitHub: https://github.com/m-labs/artiq
- Birmingham Lab: https://github.com/cnourshargh/Bham-ARTIQ-examples

  Repository of basic ARTIQ code from the University of Birmingham. Some of our examples are based on their work.

- Vutha Lab: https://github.com/vuthalab/artiq/tree/main

  Repository of ARTIQ code from Amar Vutha's group at the University of Toronto. Some of our examples are based on their work.

- Duke ARTIQ Extensions (DAX): https://gitlab.com/duke-artiq/dax/-/wikis/home
  
  DAX is a library developed by the Duke Quantum Center that extends the capabilities of ARTIQ. Initially created as a framework to develop modular control software for ARTIQ-based quantum control systems. Users can implement modular control software for their ARTIQ projects using the DAX framework or use other components and utilities provided by DAX in existing projects.

## UNB Variant of ARTIQ (system configuration from M-Labs)
- FPGA: Sinara 1124 Processor "Kasli" 2.0 (core device)
- TTL: 4x Sinara 2128 (SMA), 8-channel isolated DIOs
- DDS: 1x Sinara 4410 "Urukul" (4x AD9910)
- DAC: 1x Sinara 5432 DAC "Zotino" (32-channel, 16-bit, &pm;10 V)
- DAC Adaptor: 1x Sinara 5518 BNC-IDC (8 DAC outputs)
- DAC Adaptor: 3x Sinara 5528 SMA-IDC (24 DAC outputs)
- ADC: 1x Sinara 5108 Sampler (8-channel single-ended ADC)
- Software version installed on Lab PC: ARTIQ v7.8176.6fbfa12 (as of March 1, 2024)
- Software versions tested elsewhere: v7.8173.ff97675 (office PC)

**Note that the major software version (ARTIQ v7 here) must match the major version of the firmware and gateware installed on the core device.** The software version can be obtained by running `artiq_run --version` from the command line, the gateware version can be obtained from the bootloader during startup (see instructions for using PuTTY).

## QSUM Host configuration
- Machine: Intel(R) Core(TM) i7-10700 CPU @ 2.90GHz
- Operating System: Windows 10, 11 (x64)
- Python version: 3.10.11

## Installing ARTIQ using Conda
Following the instructions in the ARTIQ manual, we used Conda to install ARTIQ and create the neccessary virtual environment. First install Anaconda (or the lighter Miniconda). Note that, on a Windows machine, before `conda` is recognized as a command in the terminal, one must add the location of the corresponding executable `conda.exe` to the `Path` system environment variable. For our installation of Miniconda, the location is `C:\ProgramData\Miniconda3\Scripts\`

Open a terminal as **administrator** (right click the terminal app and select "Run as Administrator"), then run the following commands:

```console
conda config --prepend channels https://conda.m-labs.hk/artiq
conda config --append channels conda-forge
conda create --name artiq-7 artiq
```

This will create a virtual environment called "artiq-7" and install all of the required ARTIQ drivers. Note that https://conda.m-labs.hk/artiq/ always has the latest drivers, which will update over time. To install an earlier version, such as ARTIQ v6, use https://conda.m-labs.hk/artiq-legacy/.

To delete a virtual environment, run:
```console
conda env remove --name [NAME]
```

To view the list of virtual environments available on your machine, run:
```console
conda env list
```

To activate the artiq-7 virtual environment, run:
```console
conda activate artiq-7
```

To deactivate an environment, run:
```console
conda deactivate
```

Check to make sure the software has installed correctly by running:
```console
(artiq-7) artiq_run --version
```
This should return the current version of the ARTIQ firmware (e.g. ARTIQ v7.8176.6fbfa12).

If you encounter the error "ModuleNotFoundError: No module named 'artiq'", the package installation is likely incomplete. Navigate to the miniconda installation folder: `C:\ProgramData\miniconda3\envs\artiq-7\site-packages` and copy all of the contents to the folder `C:\ProgramData\miniconda3\envs\artiq-7\Lib\site-packages`. Python only recognizes the packages in this `\Lib` when running scripts from the command line.

## Setting up the network connection with the core device
Each ARTIQ installation is delivered with a unique device database file `device_db.py` that defines all the devices and hardware configurations specific to your system. The device database is a Python dictionary whose keys are the device names, and values can have several types. This file is also specifies the IP address of the Sinara core processor (Kasli) used by the host machine to communicate with the core. By default the IP address is `192.168.1.75`

Check if you can communicate with the Kasli core device through the terminal by running:
```console
ping 192.168.1.75
```
If the ping fails with a timeout, its possible the network adaptor is not configured correctly to communicate with the core device, which requires the adaptor to have a fixed IP address. In this case, configure its TCP/IPv4 properties to use the following: `IP Address = 192.168.1.1`, `Subnet Mask = 255.255.255.0`, leave the `Default gateway` blank. We chose an IP address with the same root `192.168.1` as the core device.

The IP address of the core device can be changed with:
```console
artiq_coremgmt -D 192.168.1.75 config write -s ip [new ip]
```

You must reboot (power cycle) the ARTIQ core for this change to take effect. Make sure to update the new address in `device_db.py` and configure the fixed IP address of the network adaptor with the same root.

## Overview of ARTIQ software
The ARTIQ software package includes several components, including:
1. The ARTIQ language in `\artiq\language\`, which contains `core.py` and `environment.py`.
2. The ARTIQ core device and drivers in `\artiq\coredevice\`
3. The ARTIQ frontend in `\artiq\frontend\`, including the `artiq_run`, `artiq_master`, `artiq_dashboard`, and `artiq_session` tools.
4. An extensive set of examples in `\artiq\examples\`

Depending on your system and installation of Anaconda/Miniconda, the ARTIQ folder can be found in one of the following directories:
- `C:\ProgramData\Miniconda3\envs\artiq-7\Lib\site-packages\artiq\`
- `C:\Users\NAME\.conda\envs\artiq-7\Lib\site-packages\artiq\`
- `~\anaconda3\envs\artiq-7\lib\python3.10\site-packages\artiq\`

The location of your ARTIQ folder can also be found by running the following in the artiq-7 virtual environment:
```console
python -c "import artiq; print(artiq.__path__[0])"
```

The ARTIQ language is a Python extension that contains all the device-independent functionality of ARTIQ. It includes the classes that experiments are meant to inherit (`EnvExperiment`), as well as methods (`build()`, `prepare()`, and `run()`), real-time commands (`break_realtime()`, `now_mu()`, `delay()`) and constructs (`with parallel` and `with sequential`).

The ARTIQ core device ("Kasli") is an FPGA-based hardware component that contains a softcore CPU tightly coupled with the so-called RTIO core that provides precision timing. The CPU executes Python code that is statically compiled by the ARTIQ compiler, and communicates with the core device peripherals (TTL, DDS, etc.) over the RTIO core. This architecture provides high timing resolution, low latency, low jitter, high level programming capabilities, and good integration with the rest of the Python experiment code.

The ARTIQ core drivers are the header files containing low-level code for communicationg with each hardware peripherals (TTL, DDS, DAC, ADC) that can be installed in the ARTIQ chassis. The [core device driver reference](https://m-labs.hk/artiq/manual/core_drivers_reference.html) and the header files are the best place to look to understand how to control device in software.

Along with the devices is a device database file called `device_db.py`. It contains the hardware configurations for the core device and all peripherals installed on your ARTIQ system. This file needs to be constructed specifically for each ARTIQ system variant and major software release (ARTIQ-7 in our case). M-Labs provided this file with our "UNB" variant. Examples of this file can be found in `\artiq\examples\`.

## Implementing stand-alone experiments with artiq_run
The `artiq_run` utility is a simple stand-alone tool designed to execute scripts containing experiments. It bypasses the ARTIQ management system. `artiq_run` can be run from the terminal or called directly from a script (see below). For a Python script called `MyExperiment.py`, navigate to the file location and from the terminal run:

```console
artiq_run MyExperiment.py
```

Optional arguments include `--device-db` for specifying the location of the device database, and `-o` for specifying the output path of an HDF5 file. For example:

```console
artiq_run --db_device MyDevice_db.py -o MyOutput.hdf5 MyExperiment.py
```

More details can be found in the ARTIQ manual under [Utilities](https://m-labs.hk/artiq/manual/utilities.html).

A basic ARTIQ experiment is constructed as follows:

```Python
from artiq.experiment import * #Imports the artiq language and device drivers

class MyExperiment(EnvExperiment): #Defines a new experiment class called "MyExperiment". Inherits from the artiq.language.environment.EnvExperiment class.
	def build(self): #Initialization method to request arguments and devices.
		self.setattr_device("core") #Sets the core device as an attribute.
		self.setattr_device("DEV") #Sets a peripheral device called DEV as an attribute.

	def prepare(self): #Optional entry point for pre-computing data necessary for running the experiment. Must not interact with ARTIQ hardware.
		...prepare something...

	@kernel #Decorator to identify methods that use hardware and real-time commands
	def run(self): #The main entry point of the experiment. May interact with ARTIQ hardware.
		self.core.reset() #Resets the core device, including the rtio clock.
		self.DEV.init() #Initialize the device DEV (init command will vary with device).
		self.core.break_realtime() #Moves the time cursor forward to prevent an RTIO underflow.
		...run something...
```

Some simple examples of this structure are shown in `ttl_out.py` and `dac.py`. These scripts can be run from the terminal using `artiq_run`.

Alternatively, a simple way of running ARTIQ scripts directly from your IDE is to add the following code to the end of the file:
```python
if __name__ == "__main__":
	from artiq.frontend.artiq_run import run
	run()
```

## Setting up VS Code to run experiments with ARTIQ

We use VS Code on Windows as our IDE.

The default terminal in VS Code is Windows PowerShell. PowerShell does not support remote activation of virtual environments. To activate the `conda` virtual environment, we had to switch the default terminal to the Command Prompt using the following setting:

```python
"terminal.integrated.defaultProfile.windows": "Command Prompt"
```

Additionally, we use the `code-runner` extension in VS Code to force scripts to execute in the terminal: 
```python
"code-runner.runInTerminal": True
```

## Using the ARTIQ management system
The management system is the high-level part of ARTIQ that schedules experiments, manages devices and scan parameters, distributes datasets between experiments, and stores the results. For now, **we do not use the management system**. Our code is distributed among several python scripts and executed using the standalone `artiq_run` utility that bypasses the management system.


### Getting started with ARTIQ master and dashboard

The master is the central program in the management system that schedules and executes experiments. The dashboard is a graphical user interface (GUI) that connects to the master and controls it. To make use of these tools:
1. Create a folder somewhere called `artiq-master\`. Place a copy of the `device_db.py` inside. Create a subfolder called `repository\`. Place your experiment scripts in `artiq-master\repository\`.
2. In a terminal window, navigate to `artiq-master\` and run: `artiq_session`
3. The dashboard GUI should appear. In the `Explorer` tab on the right, you should find a list of all of your experiments. Note that they are listed by the name of the experiment class, not the script file names.  From here you can select a file and submit it to the scheduler queue by clicking `Submit`. Datasets created in your code are automatically stored in `\artiq-master\results\` in HDF5 format.

See [Getting started with the management system](https://m-labs.hk/artiq/manual/getting_started_mgmt.html?highlight=master) in the ARTIQ manual for more details.

We note that the manual says to run `artiq_master` from a terminal while in the `artiq-master\` folder, and in a seperate terminal run `artiq_dashboard`. When we do this we encounter the error: `"artiq.dashboard.moninj: failed to connect to moninj. Is aqctl_moninj_proxy running?"`. This can be fixed by running `artiq_ctlmgr` in a third terminal. A simpler solution is to use the frontend tool `artiq_session`, which runs `artiq_master`, `artiq_dashboard`, and `artiq_ctlmgr` in sequence from the same terminal.


## Notes, Tips, and Observations

- The ARTIQ compiler / kernel code supports a subset of the Python 3.5 language. There are a number of differences that can lead to exceptions and bugs. For a complete description of (un)supported features, see https://gitlab.com/duke-artiq/dax/-/wikis/ARTIQ/Python-subset-for-kernels

- Aliases for peripheral devices can be defined within the device database file `device_db.py`. In the global `device_db` dictionary, if an entry is a string, that string is used as a key for another lookup in the device database. This is a useful way of renaming device objects. For example:

```python
device_db = {
	# Standalone peripherals
	"ttl0": {
		"type": "local",
		"module": "artiq.coredevice.ttl",
		"class": "TTLInOut",
		"arguments": {"channel": 0x000000}
		},
    "urukul_ch0": {
		"type": "local",
		"module": "artiq.coredevice.ad9910",
		"class": "AD9910",
		"arguments": {
			"pll_n": 32,
			"chip_select": 4,
			"cpld_device": "urukul0_cpld",
			"sw_device": "ttl_urukul0_sw0"
			}
		},
	"zotino": {
		"type": "local",
		"module": "artiq.coredevice.zotino",
		"class": "Zotino",
		"arguments": {
			"spi_device": "spi_zotino0",
			"ldac_device": "ttl_zotino0_ldac",
			"clr_device": "ttl_zotino0_clr"
			}
		},
	"sampler": {
		"type": "local",
		"module": "artiq.coredevice.sampler",
		"class": "Sampler",
		"arguments": {
			"spi_adc_device": "spi_sampler0_adc",
			"spi_pgia_device": "spi_sampler0_pgia",
			"cnv_device": "ttl_sampler0_cnv"
			}
		},

    # Aliases
    "Trig_In": "ttl0",
	"DDS_AOM": "urukul_ch0",
	"DAC": "zotino",
	"ADC": "sampler",
}
```

Then within the `build()` method of your experiment, these devices can be called by their aliases:

```python
def build(self):
	"""Request devices."""
	self.setattr_device("core")
	self.setattr_device("Trig_In")
	self.setattr_device("Trig_Out")
	self.setattr_device("DDS_AOM")
	self.setattr_device("DAC")
	self.setattr_device("ADC")
```

- Since ARTIQ v7, Urukul AD9910 and AD9912 DDS frequency monitoring and setting through the dashboard is supported. However, we haven't been able to use this functionality (dashboard seems unresponsive).

- The AD9910 DDS is capable of amplitude and frequency modulation (independently and at the same time). The AD9912 cannot do either. You can use a simple form of modulation (i.e. a loop where you iterate through amplitude / frequency values) if the time step is large enough. If you want the steps between amplitudes or frequencies to be small you must write the data to the core memory beforehand using DMA functions.

- When an attribute is known to never change while the kernel is running, it can be marked as a `kernel_invariant` to enable more aggressive optimization for this specific attribute. Using kernal invariants for constant attributes of a class is a simple way of speeding up real-time operations because expensive floating-point operations are hoisted out of the main loop:
```python
class Converter:
    kernel_invariants = {"ratio"}

    def __init__(self, ratio=1.0):
        self.ratio = ratio

    @kernel
    def convert(self, value):
        return value * self.ratio ** 2
```

- **Remote Procedure Calls (RPCs)**: Kernel code can call methods defined on the host machine. However, such functions are assumed to return `None`. If a value other than `None` is returned, an exception is raised. To call a host function returning a value other than `None` its return type must be annotated using the standard Python syntax, e.g.:
```python
def return_four() -> TInt32:
    return 4
```
- The Python types correspond to ARTIQ type annotations as follows:

| Python        | ARTIQ              |
|---------------|--------------------|
| NoneType      | TNone              |
| bool          | TBool              |
| int           | TInt32 or TInt64   |
| float         | TFloat             |
| str           | TStr               |
| list of T     | TList(T)           |
| NumPy array   | TArray(T, n_dims)  |
| range         | TRange32, TRange64 |
| numpy.int32   | TInt32             |
| numpy.int64   | TInt64             |
| numpy.float64 | TFloat             |

- **Asychronous RPCs**: If an RPC returns no value, it can be invoked in a way that does not block until the RPC finishes execution, but only until it is queued. Asynchronous RPCs are particularly useful for performing minimal tasks on the host during real-time operations, e.g., storing sample data in a buffer. To define an asynchronous RPC, use the `@rpc` decorator with the "async" flag:

```python
@rpc(flags={"async"})
def record_result(x):
    self.results.append(x)
```

## Sinara "TTL"

### From the datasheet:
- Pending...

### Other notes about Sinara "TTL"
- The modes (input and output) of the TTLs are set on the boards. To change them, you must take out the board, locate the switch, and flip it. TTL modes are set in blocks of four. Our system was installed with `ttl0-3` set as input. The remaining channels `ttl4-31` are set as output.

## Sinara DDS "Ukurul"

### From the datasheet:
- Pending...

### Other notes about Sinara DDS "Ukurul"
- Time required to set frequency using `dds.set(...)` is approximately 1.25 us

## Sinara DAC "Zotino"

### From the datasheet:
- 32-channel DAC based on the AD5372BCPZ (4 groups of 8 channels)
- 16-bit resolution
- 1 MSPS shared between all channels
- Output voltage: &pm;10 V
- 3dB bandwidth: 75 kHz
- All channels can be updated simultaneously (**see below**)

### Measured performance:
- Full swing rise/fall time: 22.2 us.  
  **Conditions**: Measured time 10%-90% rise/fall time for a jump from -10 V to +10 V. DAC output is remarkably linear between target values.
- Maximum onset delay: 11.2 us.  
  **Conditions**: 0 to 10 V jump, time to reach 5 V relative to parallel rtio command. Measured relative to leading edge of `ttl.pulse(100*us)`
- Max. Slew rate: 17.8 V/22.2 us = 0.8 V/us
- Min. output: -10.0000 V (using `set_dac()` command)
- Max. output:  +9.9998 V (using `set_dac()` command)
- Voltage resolution: ~0.3 mV
- Voltage noise level: ~1-2 mV RMS
- Voltage offset: 0-25 mV (depending on channel)
 
### Other notes about the Sinara "Zotino":
- All 32 channels cannot be updated simultaneously without throwing an RTIOUnderflow. It seems only blocks of 8 channels can be done at a time.
- When updating 4 channels in a block, the minimum delay required before updating the next 4 channels is ~4 us. Otherwise a busy error is reported. 
- When updating 8 channels in a block, the minimum delay required before updating the next 8 channels is ~8 us. Otherwise a busy error is reported.
- Less delay is required when updating fewer channels.
- To avoid RTIO underflow errors in a sequence, we found it's best to update a max of 4 channels in a block with ~20 us between updates.

## Sinara ADC "Sampler"

### From the datasheet:
- Channels: 8
- Resolution: 16-bit. 
- Sample rate: up to 1.5 MHz (all channels simultaneously)
- Sustained aggregate data rate in single-EEM mode (8 channel readout): ~700 kHz  
- Bandwidth: 200 kHz -6 dB bandwidth for gain = 0-2,
  90kHz for gain = 3
- Input ranges: &pm;10 V (gain = 0), &pm;1 V (gain = 1), &pm;100 mV (gain = 2), &pm;10 mV (gain = 3)
- DC input impedance:  
  Termination off: 100k from input signal and ground connections to PCB ground.  
  Termination on: signal 50 Ohm terminated to PCB ground, input ground shorted to PCB ground.
- ADC: LTC2320-16
- PGIA: AD8253

**Note that the bandwidth specifications on this page are for the hardware only; the ARTIQ kernel and RTIO overhead make the effective sample rate lower.**

### Measured performance:
- Highest sample rate:   
  2 chs: 104 kHz  
  4 chs:  92 kHz  
  6 chs:  84 kHz  
  8 chs:  64 kHz  
  **Conditions**: data acquired in machine units using `self.sampler0.sample_mu(...)`. Converted to Volts using `adc_mu_to_volt(...)`. All gains = 0. Tested for repeatability. See `Sampler_Fast.py`

### Other notes about Sinara "Sampler":
- Channels are read in reverse order
- An even number of channels must be recorded, starting from channel 7 down (i.e., minimum channels: 7, 6)
- An even number of samples per channel must be recorded
- Sampler seems to hang or crash on long acquisitions (100 kHz, 1 s, 2 chs)
