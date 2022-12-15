import sys, os, getopt, csv

def get_log_outputs_from_lines(log_lines, delimeter_text, trailing_path):
  log_outputs = []
  for line in log_lines:
    output = []
    try:
      line = line.strip()
      output = line.split(delimeter_text)
      output[1] = output[1].replace(trailing_path, "")
    except:
      print("ignoring non standard line")
    else:
      if verify_output(output):
        log_outputs.append(output)
      else:
        print("ignoring non standard line")
  return log_outputs;

def verify_output(output):
  if(len(output) != 3 ):
    return False
  if(output[0].isdigit() != True):
    return False
  return True
  

def get_log_outputs(log_file, delimeter_text, trailing_path):
  fp = open(log_file, 'r')
  log_lines = fp.read().splitlines()
  fp.close()
  return get_log_outputs_from_lines(log_lines, delimeter_text, trailing_path)
  
  
def write_output(output_file, outputs):
  fp = open(output_file, 'w', newline = '')
  writer = csv.writer(fp)
  writer.writerow(["line", "file", "message"])
  for output in outputs:
    writer.writerow(output)
  fp.close()


def main(argv):
  
  input_file = "";
  output_file = "parser_output.csv"
  delimeter_text = "<<>>"
  remove_path = ""
  
  try:
    opts, args = getopt.getopt(argv,"i:o:d:r:")
    for opt, arg in opts:
      if opt == '-i':
        input_file = arg
      if opt == '-o':
        output_file = arg
      if opt == '-d':
        delimeter_text = arg
      if opt == '-r':
        remove_path = arg
    if input_file == "":
      print ('-i <inputfile> is a required parameter')
      sys.exit(2)
  except getopt.GetoptError:
    print ('parser.py -i <inputfile> -o <outputfile> -d <delimiter> -r <remove_path>')
    sys.exit(2)
  
  outputs = get_log_outputs(input_file, delimeter_text, remove_path)
  write_output(output_file, outputs)
  
if __name__ == "__main__":
   main(sys.argv[1:])
