import unittest, os, csv

target = __import__("doxygen_parser")

class UnitTests(unittest.TestCase):
    def test_all_correct_lines(self):
      lines = [];
      # Create two correct log lines
      lines.append('198<<>>/src/test1.cpp<<>>warning: this is first warning')
      lines.append('100<<>>/src/test2.cpp<<>>warning: this is second warning')
      
      # Act
      parser_outputs = target.get_log_outputs_from_lines(lines, '<<>>','/src/')
      
      
      # assert that the output has 2 lines
      self.assertEqual(len(parser_outputs), 2)

    def test_malformed_lines(self):
      lines = [];
      
      # Create one wel formed line and one malformed line
      lines.append('198<<>>/src/test1.cpp<<>>warning: this is first warning')
      # No line number
      lines.append('/src/test2.cpp<<>>warning: this is second warning')
      # line is not a digit
      lines.append('Hello<<>>/src/test2.cpp<<>>warning: this is second warning')
      
      # Act
      parser_outputs = target.get_log_outputs_from_lines(lines, '<<>>','/src/')
      
      # assert that only one well formed line will be output
      self.assertEqual(len(parser_outputs), 1)
    
    def test_delimeter(self):
      lines = [];
      
      # Create one line with delimeter <<>>
      lines.append('198<<>>/src/test1.cpp<<>>warning: this is first warning')
      # line with delimer ','
      lines.append('200,/src/test2.cpp,warning: this is second warning')
      
      # Act
      parser_outputs = target.get_log_outputs_from_lines(lines, '<<>>','/src/')
      
      # assert that only one line with correct delimeter <<>> output
      self.assertEqual(len(parser_outputs), 1)

class IntegerationTests(unittest.TestCase):
    # Test if the parse correctly open the file read it and output logs
    def test_input_file_read(self):
      # Create temporary file which will serve as input log file
      fp = open('parser_tests_dump.log','w')
      fp.write('198<<>>/src/test1.cpp<<>>warning: this is first warning\n')
      fp.write('100<<>>/src/test2.cpp<<>>warning: this is second warning')
      fp.close();
      
      # Act
      parser_outputs = target.get_log_outputs(fp.name, '<<>>', '/src/')
      
      # assert that the output has 2 lines
      self.assertEqual(len(parser_outputs), 2)
      
      # delete the file
      os.remove(fp.name)
    
    # Test if the outputs correctly written to output file
    def test_write_output(self):
      
      # create two output entries
      outputs =[['198','/src/test1.cpp','This is first warning'],['100','/src/test2.cpp','This is second warning']]
      
      # Act
      target.write_output('parser_tests_dump.csv',outputs)
      
      # read the output csv file
      fp = open('parser_tests_dump.csv','r')
      reader = csv.reader(fp)
      
      column_headings = reader.__next__()
      line1 = reader.__next__()
      line2 = reader.__next__()
      
      # assert column headings 
      self.assertEqual(column_headings[0],'line')
      self.assertEqual(column_headings[1],'file')
      self.assertEqual(column_headings[2],'message')
      
      # verify rows data
      self.assertEqual(line1[0],outputs[0][0])
      self.assertEqual(line1[1],outputs[0][1])
      self.assertEqual(line1[2],outputs[0][2])
      
      self.assertEqual(line2[0],outputs[1][0])
      self.assertEqual(line2[1],outputs[1][1])
      self.assertEqual(line2[2],outputs[1][2])
      

      # close the resources
      fp.close()
      os.remove('parser_tests_dump.csv')
      
    def test_main(self):
      exceptionRaised = False
      
      # Act
      try:
        target.main('')
      except SystemExit: 
        exceptionRaised = True
      
      # Verify that the SystemExit exception was raised when no input file was provided
      self.assertTrue(exceptionRaised)

if __name__ == '__main__':
  unittest.main()
