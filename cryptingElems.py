
_alfa = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
         'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def code_correct(code):
        # code - string representing letter replacement pattern
    # must contain every letter of alphabet in uppercase
    if 26 == len(set(code)) and all( let.isalpha() and let.isupper() for let in code ):
       return code
    raise WrongInput()
    
# def get_code(self): return self._code

def code_symmetric(code):
    # additional verification is conducted - is the code symmetric
    if all( _alfa.index(code[i]) == code.index(_alfa[i]) for i in range(len(code)) ):
        return True
    raise WrongInput('code for stator not symmetric')


class Stator(object):
    '''
    element on the end or beginning of block of wheels
    connects letters in pairs and turns signal back to last wheel
    its pattern is constant
    '''
    def __init__(self, code):   
        if code_correct(code) and code_symmetric(code):
            self._code = code
    
    def output(self, letter):
        return self._code[ _alfa.index(letter) ]


class Wheel(object):
    '''
    class handles encrypting wheel
    its got 26 possible positions (0-25)
    each posiiton represents different letter replacement order
    wheel will generate output for each letter
    '''
    def __init__(self, code):
        self._code = code_correct(code)
        self._position = 0 # default position is 0

    def get_position(self): return self._position

    def set_position(self, _desired):
        assert str(_desired).isnumeric(), "invalid type"
        assert 0 <= _desired <= 25, "invalid position"
        while self._position != _desired:
            self.click()

    def click(self):
        # function responsible for changing rotor position by one every step
        # after completing full rotation function returns True, normally False
        # this information is used by Barell method, for another wheel to move
        self._code = self._code[-1] + self._code[:-1]
        self._position += 1
        if self._position > 25:
            self._position -= 26
            return True
        return False
        
    # depending on signal propagating forwards or backwards
    # two functions are used, to retreive letter on code responding to letter from alphabet 
    # or the opposite
    def output_forward(self, letter):
        return self._code[ _alfa.index(letter) ]

    def output_backward(self, letter):
         return _alfa[ self._code.index(letter) ]


class Barell(object):
    '''
    Group of wheels
    Letter goes througt them in two directions
    lets make elements a public list, so one can modify it and access members freely
    '''
    def __init__(self, wall_code='RDOBJNTKVEHMLFCWZAXGYIPSUQ'):
        self.elements = []
        self._reflector = Stator(wall_code)

    def add_wheel(self, *codes):
        # function for adding rotors to Barrel unit
        # provided with any number of codes will create Wheel objects and add them to Barell
        for code in codes:
            self.elements.append(Wheel(code))

    def set_wheels(self, sequence=None):
        # method for setting wheel positions
        # call empty to set wheels to zeros
        # otherwise provide input corresponding with count of wheels
        if sequence == None:                                         
            for el in self.elements:
                el.set_position(0)
        elif len(sequence) == len(self.elements):
            for el, n in zip(self.elements, sequence):
                el.set_position(int(n))
        else:
            raise WrongInput()

    def get_positions(self):
        return [el.get_position() for el in self.elements]
        
    def _operation_click(self):
        # function for modelling turning of wheels on every press of button
        # the first rotor moves one step every round
        # every another rotor does one step after previous rotor completed full rotation
        for el in self.elements:
            if el.click() == False:
                break

    def output(self, letter):
        self._operation_click()             # click occurs before crypting
        # signal goes through set of wheels, than turnd back on stator and comes backwards througn wheels
        for el in self.elements:
            letter = el.output_forward(letter)
        letter = self._reflector.output(letter)
        for el in self.elements[::-1]:
            letter = el.output_backward(letter)
        return letter
       
    
class PlugBoard(object):
    '''
    Class representing an electric board where any two letters can be connected by wire resulting with replacing them 
    this element is symmetrical
    '''
    def __init__(self, *pairs):         
        # accepts any number of pairs - 2-letter strings telling which letters to replace
        self._replacement_dict = {}
        self._fill_dict(*pairs)

    def _fill_dict(self, *pairs):
        for pair in pairs:
            self._create_pair(pair)

    def _create_pair(self, pair):            # each pair is added to dictionary
        pair = pair.upper()
        if len(pair) != 2 or pair[0] in self._replacement_dict or pair[1] in self._replacement_dict or pair[0] == pair[1]:
            raise WrongInput
        pair = pair.upper()
        self._replacement_dict[pair[0]] = pair[1]
        self._replacement_dict[pair[1]] = pair[0]

    def output(self, letter):
        return self._replacement_dict.get(letter, letter)


class WrongInput(Exception):
    pass

def test():
    pass#     "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
             #'RDOBJNTKVEHMLFCWZAXGYIPSUQ'
    wh = Wheel('RDOBJNTKVEHMLFCWZAXGYIPSUQ')
    wh1 = Wheel('RDOBJNTKVEHMLFCWZAXGYIPSUQ')
    qq = Barell()
    p_list = ['re','po']
    bb = PlugBoard(*p_list)
    print(bb.output('a'))
    print(bb._replacement_dict)


if __name__=="__main__":
    test()
    print(" finished")

