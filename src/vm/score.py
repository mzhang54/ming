import os
import sys

# TODO: Add Weights to each test
# TODO: userprog tests

USERPROG_TESTS = ['args-none', 'args-single', 'args-multiple', 'args-many', 'args-dbl-space', 'create-empty', 'create-long', 'create-normal', 'create-exists', 'open-missing', 'open-normal', 'open-twice', 'read-normal', 'read-zero', 'write-normal', 'write-zero', 'close-normal', 'exec-once', 'exec-multiple', 'exec-arg', 'wait-simple', 'wait-twice', 'exit', 'halt', 'multi-recurse', 'rox-simple', 'rox-child', 'rox-multichild', 'close-stdin', 'close-stdout', 'close-bad-fd',
                  'close-twice', 'read-bad-fd', 'read-stdout', 'write-bad-fd', 'write-stdin', 'multi-child-fd', 'create-bad-ptr', 'exec-bad-ptr', 'open-bad-ptr', 'read-bad-ptr', 'write-bad-ptr', 'create-bound', 'open-boundary', 'read-boundary', 'write-boundary', 'create-null', 'open-null', 'open-empty', 'sc-bad-arg', 'sc-bad-sp', 'sc-boundary', 'sc-boundary-2', 'exec-missing', 'wait-bad-pid', 'wait-killed', 'bad-read', 'bad-write', 'bad-jump', 'bad-read2', 'bad-write2', 'bad-jump2']
VM_TESTS = ['pt-grow-stack', 'pt-grow-stk-sc', 'pt-big-stk-obj', 'pt-grow-pusha', 'pt-bad-addr', 'pt-bad-read', 'pt-write-code', 'pt-write-code2',
            'pt-grow-bad', 'page-linear', 'page-parallel', 'page-shuffle', 'page-merge-seq', 'page-merge-par']
FILESYS_TESTS = ['sm-create', 'sm-full', 'sm-random', 'sm-seq-block', 'sm-seq-random', 'lg-create', 'lg-full', 'lg-random', 'lg-seq-block', 'lg-seq-random', 'syn-read', 'syn-write', 'syn-remove']

class Grader(object):
    def __init__(self, valid_tests, file_name):
        self.file_name = file_name
        self.valid_tests = valid_tests
        self.all_lines = self.read_file()

        self._start_line = None
        self._end_line = None
        self.test_lines = None
        self.all_tests = {}

        self.read_all_tests()

        # self.all_tests = self.read_tests()

        self.__PASS = 'PASS'
        self.__FAIL = 'FAIL'

    def read_file(self):

        all_lines = list(open(self.file_name))

        return all_lines

    def read_all_tests(self):
        self.all_tests = {}
        self.test_lines = []

        self._start_line = self.all_lines.index(
            'SUMMARY OF INDIVIDUAL TESTS\n') + 4

        self._end_line = self._start_line + self.all_lines[self._start_line:].index(
            '- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - \n') - 1

        for line in self.all_lines[self._start_line:self._end_line]:
            line_list = line.rstrip("\n\r").split('/')
            if(len(line_list) >= 4 and line_list[0][0] == '\t'):
                test_name = line_list[-1]
                test_score = int(line_list[0][-2:])
                test_max_score = int(line_list[1][0:2])

                self.all_tests[test_name] = [test_score, test_max_score]

                self.test_lines.append(line)

    def print_all_tests(self):
        for test in self.all_tests.keys():
            print('{0:20} {1}/{2}'.format(
                test, self.all_tests[test][0], self.all_tests[test][1]))

    def print_valid_tests(self):
        print('{0:21} {1}/{2}'.format(
                    '     Test Name', 'Score', 'Max Score'))
        print '   -------------------------------------'
            
        for test in self.valid_tests:
            if(self.all_tests[test][0] == self.all_tests[test][1]):
                print('{0:25} {1}/{2}'.format(
                    '     ' + test, self.all_tests[test][0], self.all_tests[test][1]))
            else:
                print('{0:25} {1}/{2}'.format(
                    '**   ' + test, self.all_tests[test][0], self.all_tests[test][1]))

    def calculate_grade(self):
        score = 0
        max_score = 0
        ctr = 0
        for test in self.valid_tests:
            score = score + self.all_tests[test][0]
            max_score = max_score + self.all_tests[test][1]
            if(self.all_tests[test][0] == self.all_tests[test][1]):
                ctr = ctr + 1

        index = self.all_lines.index('SUMMARY BY TEST SET\n') + 10
        
        print '--------------------------------------------------------'
        print 'SUMMARY: '
        print "Number of tests passed : ", ctr, "/", len(self.valid_tests)
        print "Score/Max Score        : ", score, "/", max_score
        print "Total Score            : ", round(score*100.0/max_score, 2), "%"
        print '--------------------------------------------------------'


    def test_grader(self):

        def get_original_grader_score(self):
            start_line = self.all_lines.index('SUMMARY BY TEST SET\n') + 4
            end_line = start_line + 5
            lines = []
            print "----------------------------------------"
            print "ORGINAL GRADER"
            print "----------------------------------------"
            for i in range(start_line, end_line):
                lines.append(self.all_lines[i][0:53])
                print self.all_lines[i],
            print self.all_lines[i+1],self.all_lines[i+2]
            return lines

        def get_current_grader_score(self):
            lines = []

            vm_functionality =['pt-grow-stack', 'pt-grow-stk-sc', 'pt-big-stk-obj', 'pt-grow-pusha', 'page-linear', 'page-parallel', 'page-shuffle', 'page-merge-seq', 'page-merge-par',
                              'page-merge-mm', 'page-merge-stk', 'mmap-read', 'mmap-write', 'mmap-shuffle', 'mmap-twice', 'mmap-unmap', 'mmap-exit', 'mmap-clean', 'mmap-close', 'mmap-remove']

            vm_robustness = ['pt-bad-addr', 'pt-bad-read', 'pt-write-code', 'pt-write-code2', 'pt-grow-bad', 'mmap-bad-fd', 'mmap-inherit',
                             'mmap-null', 'mmap-zero', 'mmap-misalign', 'mmap-over-code', 'mmap-over-data', 'mmap-over-stk', 'mmap-overlap']

            userprog_functionality = ['args-none', 'args-single', 'args-multiple', 'args-many', 'args-dbl-space', 'create-empty', 'create-long', 'create-normal', 'create-exists', 'open-missing', 'open-normal', 'open-twice',
                                      'read-normal', 'read-zero', 'write-normal', 'write-zero', 'close-normal', 'exec-once', 'exec-multiple', 'exec-arg', 'wait-simple', 'wait-twice', 'exit', 'halt', 'multi-recurse', 'rox-simple', 'rox-child', 'rox-multichild']

            userprog_robustness = ['close-stdin', 'close-stdout', 'close-bad-fd','close-twice','read-bad-fd','read-stdout','write-bad-fd','write-stdin','multi-child-fd','create-bad-ptr','exec-bad-ptr','open-bad-ptr','read-bad-ptr','write-bad-ptr','create-bound','open-boundary','read-boundary','write-boundary','create-null','open-null','open-empty','sc-bad-arg','sc-bad-sp','sc-boundary','sc-boundary-2','exec-missing','wait-bad-pid','wait-killed','bad-read','bad-write','bad-jump','bad-read2','bad-write2','bad-jump2']

            filesys = ['sm-create', 'sm-full', 'sm-random','sm-seq-block','sm-seq-random','lg-create','lg-full','lg-random','lg-seq-block','lg-seq-random','syn-read','syn-write','syn-remove']

            def get_section_score(self, test, test_name):
                score = 0
                max_score = 0
                ctr = 0
                for test in test:
                    score = score + self.all_tests[test][0]
                    max_score = max_score + self.all_tests[test][1]
                    ctr = ctr + 1

                return ('{0:45} {1:3}/{2:3}'.format(test_name, score, max_score))


            lines.append(get_section_score(self, vm_functionality, "tests/vm/Rubric.functionality") )
            lines.append(get_section_score(self, vm_robustness, "tests/vm/Rubric.robustness") )
            lines.append(get_section_score(self, userprog_functionality, "tests/userprog/Rubric.functionality") )
            lines.append(get_section_score(self, userprog_robustness, "tests/userprog/Rubric.robustness") )
            lines.append(get_section_score(self, filesys, "tests/filesys/base/Rubric") )

            return lines

        original_grader_lines = get_original_grader_score(self)
        print "----------------------------------------"
        print "MATCHED ORGINAL GRADER"
        print "----------------------------------------"
        for l in original_grader_lines:
            print l

        current_grader_lines = get_current_grader_score(self)
        print "\n----------------------------------------"
        print "MACTHED NEW GRADER"
        print "----------------------------------------"
        for l in current_grader_lines:
            print l

        print "\n----------------------------------------"

        if(original_grader_lines == current_grader_lines):
            print "-> TEST PASSED"
            return True
        else:
            print "-> TEST FAILED"
            return False

if __name__ == "__main__":

    grade_file_name = "build/grade"

    if(not os.path.isfile(grade_file_name)):
        print "ERROR: cannot find grade file in build directory"

        print "Troubleshooting: "
        print "   1. Make sure score.py is in the pintos/src/vm directory.", "( Current Script Location: ", os.getcwd(), " )"
        print "   2. Make sure you ran \"make grade\" from pintos/src/vm,  before running this script"

        print '--------------------------------------------------------'
        print '--------------------------------------------------------'
        print 'SUMMARY: '
        print "Total Score            : ", 0, "%"
        print '--------------------------------------------------------'
        sys.exit()

    g = Grader(valid_tests=USERPROG_TESTS + VM_TESTS + FILESYS_TESTS, 
               file_name=grade_file_name)

    g.print_valid_tests()
    g.calculate_grade()

    print "*** Note: The grader does not check if lazy loading has been implemented; you may lose score later if it has not been implemented ***"

