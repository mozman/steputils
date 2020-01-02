from steputils.stepfile import Factory as sf  # (S)TEP-file (F)actory
from pyparsing import ParseException

OUTDIR = 'C:\\Users\\manfred\\Desktop\\Outbox\\'
FNAME = 'example.p21'

# Create a new STEP-file:
stepfile = sf.new()

# Create new data section:
data = stepfile.new_data_section()

# Add entity instances to data section:
data.add(sf.simple_instance('#1', name='APPLICATION', params=('MyApp', 'v1.0')))

# Set required header entities:
stepfile.header.set_file_description(('Example STEP file', 'v1.0'))
stepfile.header.set_file_name(name=FNAME, organization=('me', 'myself'), autorization='me')
stepfile.header.set_file_schema(('NONE',))

# Write STEP-file to file system:
stepfile.save(OUTDIR+FNAME)

# Read an existing file from file system:
try:
    stepfile = sf.readfile(OUTDIR+FNAME)
except IOError as e:
    print(str(e))
except ParseException as e:
    # Invalid STEP-file
    print(str(e))
else:
    print(f'File {FNAME} is a valid STEP-file')
