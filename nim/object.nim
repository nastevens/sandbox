type
    TPerson = object of TObject
        name*: string
        age: int

var
    jim: TPerson

jim = TPerson("Jim", 23)

template `!=` (a, b: expr): expr = 
    not (a == b)

