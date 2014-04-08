#!/bin/env python

"""
FrameRange class to handle 

usage:
    import frameRange.FrameRange as FrameRange
    FrameRange( [1,2,3]  ) # -> [1,2,3]
    FrameRange( "1-10"   ) # -> [1,2,3,4...]
    FrameRange( "1-10x2" ) # -> [1,3,5,7,9]
    FrameRange( "1-3,10" ) # -> [1,2,3,10]
    FrameRange( "1,2,10" ) # -> [1,2,10]

    FrameRange( "1-10"   ).asString() # -> "1-10"
    FrameRange( "1-10"   ).asList()   # -> [1,2,3,4...]

    FrameRange inheriting from list, so you can do:
    for frame in FrameRange( "1-10" ):
        print frame # -> 1,2,3...
"""
## ----------------------------------------------------
#   IMPORTS
## ----------------------------------------------------
import re

## ----------------------------------------------------
#   FrameRange
## ----------------------------------------------------
class FrameRange( list ) :

    def __init__( self, input ) :
        ## Convert string input to a list
        if type(input) in [str,unicode]:
            input = FrameRange.parse( input )

        super( FrameRange, self ).__init__( sorted(input) )

    def __repr__( self ) :
        return "%s(\"%s\")"%( self.__class__.__name__, self.asString() )

    def __str__( self ) :
        return self.asString()

    def asString(self):
        '''
        Return framerange as string
        '''
        if self.step and self.step!=1:
            return "%d-%dx%d" % (self.first, self.last, self.step)

        elif self.step==1:
            return "%d-%d" % (self.first, self.last)

        else:
            return ",".join( [str(i) for i in self] )

    def asList(self):
        '''
        Return framerange as list
        '''
        return list(self)


    ## ----------------------------------------------------
    #   Property
    ## ----------------------------------------------------
    @property
    def step( self ):
        '''
        Return framerange stepping value
        '''
        step = None

        for index, value in enumerate( self ):

            if index == len(self)-1:
                break

            current_step = self[index+1]-self[index]

            if step==None:
                step = current_step
            elif step != current_step:
                return None

        return step

    @property
    def first( self ):
        '''
        Return framerange lowest/first frame
        '''
        return min(self)

    @property
    def last( self ):
        '''
        Return framerange highest/last frame
        '''
        return max(self)

    ## ----------------------------------------------------
    #   Staticmethod
    ## ----------------------------------------------------
    @staticmethod
    def parse( framestring ) :
        '''
        Parse framerange from string
        '''
    
        # is it a single frame?
        try :
            value = int(framestring)
            return FrameRange( [value] )
        except :
            pass

        frames = []

        ## Break framestring into packets
        reg_list = ["^(?P<start>\d+)$",                             # 500
                    "^(?P<start>\d+)-(?P<end>\d+)$",                # 1-100
                    "(?P<start>\d+)-(?P<end>\d+)x(?P<step>\d+)"]    # 1-100x10
        
        # Eval each packet in string
        for packet in re.split(r"[,\sa-wyzA-WYZ]+", framestring ):

            # check for valid packets
            for reg in reg_list:
                
                match = re.search( reg, packet )
                
                if not match:
                    continue

                # Convert each packet to a duration and step
                # eg. 1-10x1, 240x240x1, 0-250x10
                data  = match.groupdict()
                start = data.get( 'start', 1 )
                end   = data.get( 'end', start )
                step  = data.get( 'step', 1 )
                # derive list of frames from stepped durations
                for i in range(int(start), int(end)+1, int(step)):
                    frames.append( i )

        if not frames:
            raise AssertionError( "Unable to parse framerange: '%s'" %framestring)
        
        return sorted(set(frames))


## Unittest
if __name__=="__main__":

    ## "1-10"
    frames  = range(1,11,1)
    print FrameRange( "1-10") == frames, FrameRange( "1-10")

    ## "1-10x2"
    frames = range(1,11,2)
    print FrameRange( "1-10x2") == frames, FrameRange( "1-10x2" )

    ## "1,2,7,8"
    frames = [1,2,7,8]
    print FrameRange( "1,2,7,8" ) == frames, FrameRange( "1,2,7,8" )

    ## "1-5,9"
    frames = [1,2,3,4,5,9]
    print FrameRange( "1-5,9" ) == frames, FrameRange( "1-5,9" )

    ## "1,2,8-9"
    frames = [1,2,8,9]
    print FrameRange( "1,2,8-9" ) == frames, FrameRange( "1,2,8-9" )

    ## "1 5 10"
    frames = [1,5,10]
    print FrameRange( "1 5 10" ) == frames, FrameRange( "1 5 10" )
