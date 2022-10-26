#!/usr/bin/env python
#
# file: $NEDC_NFC/util/python/nedc_pyprint_header/nedc_pyprint_duration.py
#
# revision history:
#
# 20200813 (NR): initial version
# 20200801 (JP): created a template
#
# This is a Python version of the C++ utility nedc_print_duration..
#------------------------------------------------------------------------------

# import system modules
#
import os
import sys

# import nedc_modules
#
import nedc_cmdl_parser as ncp
import nedc_debug_tools as ndt
import nedc_edf_tools as net
import nedc_file_tools as nft

#------------------------------------------------------------------------------
#
# global variables are listed here
#
#------------------------------------------------------------------------------

# set the filename using basename
#
__FILE__ = os.path.basename(__file__)

# define the location of the help files
#
HELP_FILE = \
    "$NEDC_NFC/util/python/nedc_pyprint_duration/nedc_pyprint_duration.help"

USAGE_FILE = \
    "$NEDC_NFC/util/python/nedc_pyprint_duration/nedc_pyprint_duration.usage"

#------------------------------------------------------------------------------
#
# functions are listed here
#
#------------------------------------------------------------------------------

# declare a global debug object so we can use it in functions
#
dbgl = ndt.Dbgl()

# function: main
#
def main(argv):

    # declare local variables
    #
    edf = net.Edf()

    # create a command line parser
    #
    cmdl = ncp.Cmdl(USAGE_FILE, HELP_FILE)
    cmdl.add_argument("files", type = str, nargs = '*')

    # parse the command line
    #
    args = cmdl.parse_args()

    # check the number of arguments
    #
    if len(args.files) == int(0):
        cmdl.print_usage('stdout')

    # display an informational message
    #
    print("beginning argument processing...")
     
    # main processing loop: loop over all input filenames
    #
    num_files_att = int(0)
    num_files_proc = int(0)
    total_duration = float(0.0)
    
    for fname in args.files:
     
        # expand the filename (checking for environment variables)
        #
        ffile = nft.get_fullpath(fname)

        # check if the file exists
        #
        if os.path.exists(ffile) is False:
            print("Error: %s (line: %s) %s: file does not exist (%s)" %
                  (__FILE__, ndt.__LINE__, ndt.__NAME__, fname))
            sys.exit(os.EX_SOFTWARE)

        # case (1): an edf file
        #
        if (edf.is_edf(fname)):

            # display informational message
            #
            num_files_att += int(1)
            print("  %6d: %s" %
                 (num_files_att, fname))

            # check if header information exists
            #
            if edf.get_header_from_file(fname) != None:
                
                # get duration
                #
                dur = edf.get_duration()

                # display duration value
                #
                print("   %1d (%10.2f secs): %s" %
                      (num_files_proc, dur, fname))

                # sum the total duration
                #
                total_duration += dur
                num_files_proc += int(1)

            # error message if header information does not exist
            #
            else:
                print("Error: %s (line: %s) %s: header corrupted (%s)" %
                      (__FILE__, ndt.__LINE__, ndt.__NAME__, fname))

            # cleanup the edf header memory
            #
            edf.cleanup();
                
        # case (2): a list
        #
        else:

            # display debug information
            #
            if dbgl > ndt.NONE:
                print("%s (line: %s) %s: opening list (%s)" %
                      (__FILE__, ndt.__LINE__, ndt.__NAME__, fname))

            # fetch the list
            #
            files = nft.get_flist(ffile)
            if files is None:
                print("Error: %s (line: %s) %s: error opening (%s)" %
                      (__FILE__, ndt.__LINE__, ndt.__NAME__, fname))
                sys.exit(os.EX_SOFTWARE)

            else:

                # loop over all files in the list
                #
                for edf_fname in files:

                    # expand the filename (checking for environment variables)
                    #
                    ffile = nft.get_fullpath(edf_fname)

                    # check if the file exists
                    #
                    if os.path.exists(ffile) is False:
                        print("Error: %s (line: %s) %s: %s (%s)" %
                              (__FILE__, ndt.__LINE__, ndt.__NAME__,
                               "file does not exist", fname))
                        sys.exit(os.EX_SOFTWARE)

                    if (edf.is_edf(ffile)):

                        # display informational message
                        #
                        num_files_att += int(1)
                        print("  %6d: %s" %
                              (num_files_att, edf_fname))

                        # check if header information exists
                        #
                        if edf.get_header_from_file(ffile) != None:
                
                            # get duration
                            #
                            dur = edf.get_duration()

                            # display duration value
                            #
                            print("   %1d (%10.2f secs): %s" %
                                  (num_files_proc, dur, edf_fname))

                            # sum the total duration
                            #
                            total_duration += dur
                            num_files_proc += int(1)

                        # error message if header information does not exist
                        #
                        else:
                            print("Error: %s (line: %s) %s: %s (%s)" %
                                  (__FILE__, ndt.__LINE__, ndt.__NAME__,
                                   "header corrupted", fname))

                        # cleanup the edf header memory
                        #
                        edf.cleanup();

    # display the results
    #
    print("ending processing...\n\n")
    
    print("total num files processed successfully was %1d out of %1d" %
	  (num_files_proc, num_files_att))

    print("total dur of data processed = %0.4f secs | %0.4f mins | %0.4f hrs" %
          (total_duration, total_duration / 60,
           total_duration / 3600))

    print("avg file dur = %0.4f secs | %0.4f mins | %0.4f hrs" %
          (total_duration / num_files_proc,
           total_duration / 60 / num_files_proc,
           total_duration / 3600 / num_files_proc))
          
    # exit gracefully
    #
    return True

# begin gracefully
#
if __name__ == '__main__':
    main(sys.argv[0:])
#
# end of file
