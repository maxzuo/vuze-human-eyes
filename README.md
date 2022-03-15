# vuze-human-eyes
Masks images according to how the Vuze XR camera wants its images (Vuze XR studio is super finicky).


## Setup
A python virtualenv is highly recommended. To create one, use the following commands:
```bash
python -m pip install virtualenv
python -m virtualenv venv
. ./venv/bin/activate #mac, linux
. ./venv/Scripts/activate #windows
```

Next, pip install the required packages:
```bash
pip install -r requirements.txt
```

## Usage
To run the script, use the following formula:
```bash
python mask.py --eye ./path/to/image/of/either/left/or/right/eye
```

**Remember to run the script from the same directory as the script: do not cd to another directory and try to run this script**

To add blurs, we have the following optional parameters:

```bash
python mask.py --eye ./path/to/image/of/eye --blur_edges POSITIVE_ODD_INT --blur_strength POSITIVE_FLOAT
```

As always running `python mask.py -h` will result in a useful listing of accepted parameters.