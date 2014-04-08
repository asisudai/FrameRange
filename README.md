FrameRange
==========

FrameRange class to handle framerange string inputs

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
