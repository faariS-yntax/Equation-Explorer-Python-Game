import random
import math

# Type 1 : linear algebra
# Standard form : ax + by = answer
def generate_linear_algebra_equation():
    
    # Generate coefficients for the linear equation
    x = random.randint(1, 10)
    y = random.randint(1, 10)
    a = random.randint(1, 10)
    b = random.randint(1, 10)

    # Calculate the answer
    answer = a*x + b*y
    
    # Build the equation string
    equation = f"{a}x + {b}y = {answer}"
    
    # Build the hints string
    num_additional_hints = 5 # specify the number of additional hints you want to generate
    additional_hints = [str(random.randint(1, 10)) for _ in range(num_additional_hints)]
    all_hints = [str(a), str(b), str(answer)] + additional_hints
    random.shuffle(all_hints)
    hints = ','.join(all_hints)
    
    # Calculate the possible solution
    solution = f"x = {x},y = {y}"
    
    return equation, hints, solution

# Type 2 : quadratic function
# Standard form : ax^2 + bx + c = 0
def generate_quadratic_equation():
 
    # Generate two integers p and q for the roots
    p = random.randint(1, 10)
    q = random.randint(1, 10)

    # Generate an integer a for the coefficient of x^2
    a = random.randint(1, 10)

    # Calculate b and c from the factored form (x - p)(x - q)
    b = -a * (p + q)
    c = a * p * q

    # Build the equation string (but this one is too long)
    '''
    # Use abs to remove negative sign
    if (a<0 | b>0 | c>0): # When a is negative
        equation = f"-{abs(a)}x^2 + {b}x + {c} = 0" 
    elif (a>0 | b<0 | c>0): # When b is negative
        equation = f"{a}x^2 - {abs(b)}x + {c} = 0"
    elif (a>0 | b>0 | c<0): # When c is negative
        equation = f"{a}x^2 + {b}x - {abs(c)} = 0"
    elif (a<0 | b<0 | c>0): # When a and b is negative
        equation = f"-{abs(a)}x^2 - {abs(b)}x + {c} = 0"
    elif (a<0 | b>0 | c<0): # When a and c is negative
        equation = f"-{abs(a)}x^2 + {b}x - {abs(c)} = 0"
    elif (a>0 | b<0 | c<0): # When b and c is negative
        equation = f"{a}x^2 - {abs(b)}x - {abs(c)} = 0"
    elif (a<0 | b<0 | c<0): # When a, b and c is negative
        equation = f"-{abs(a)}x^2 - {abs(b)}x - {abs(c)} = 0"
    else: # When all is positive
        equation = f"{a}x^2 + {b}x + {c} = 0"'''
        
    # Build the equation string (shorter version)
    # Bahagian ni utk print equation dlm file tu in the right format je, so dont worry much about this
    # Basic structure print euqation mcm ni : equation = f"{a}x^2 + {b}x + {c} = 0"
    equation = ""
    if a != 0:
        equation += f"{abs(a)}x^2 " if a < 0 else f"{a}x^2 "
    if b != 0:
        equation += f"- {abs(b)}x " if b < 0 else f"+ {b}x "
    if c != 0:
        equation += f"- {abs(c)} " if c < 0 else f"+ {c} "
    equation += "= 0"

    # Build the hints string
    num_additional_hints = 5 # specify the number of additional hints you want to generate
    additional_hints = [str(random.randint(1, 10)) for _ in range(num_additional_hints)]
    all_hints = [str(a), str(b), str(c)] + additional_hints
    random.shuffle(all_hints)
    hints = ','.join(all_hints)

    # Calculate the possible solution using the roots p and q
    solution = f"{p},{q}"

    return equation, hints, solution

# Type 3 : cubic function
# Standard form : ax^3 + bx^2 + cx + d = 0
def generate_cubic_equation():

    # Generate three integers p, q, and r for the roots
    p = random.randint(1, 5)
    q = random.randint(1, 5)
    r = random.randint(1, 5)
    z = random.randint(1, 10)
    
    # Generate an integer a for the coefficient of x^3
    a = random.randint(1, 10)

    # Calculate b, c, and d from the factored form (x - p)(x - q)(x - r)
    b = -a * (p + q + r)
    c = a * (p*q + p*r + q*r)
    d = -a * p * q * r

    # Build the equation string (shorter version)
    equation = ""
    if a != 0:
        equation += f"{abs(a)}x^3 " if a < 0 else f"{a}x^3 "
    if b != 0:
        equation += f"- {abs(b)}x^2 " if b < 0 else f"+ {b}x^2 "
    if c != 0:
        equation += f"- {abs(c)}x " if c < 0 else f"+ {c}x "
    if d != 0:
        equation += f"- {abs(d)} " if d < 0 else f"+ {d} "
    equation += "= 0"

    # Build the hints string
    num_additional_hints = 5 # specify the number of additional hints you want to generate
    additional_hints = [str(random.randint(1, 10)) for _ in range(num_additional_hints)]
    all_hints = [str(a), str(b), str(c), str(d)] + additional_hints
    random.shuffle(all_hints)
    hints = ','.join(all_hints)
    # Calculate the possible solution using the roots p, q, and r
    solution = f"{p},{q},{r}"

    return equation, hints, solution

def generate_equation_file(filename, num_equations):
    with open(filename, 'w') as file:
        # Write the header
        file.write("Type\tEquation\tHints\tSolution\n")
        
        for equation_type in range(1, 4):
            for _ in range(num_equations): # Generate how many equations based on how many amount we wants
                if equation_type == 1:
                    equation, hints, solution = generate_linear_algebra_equation()
                elif equation_type == 2:
                    equation, hints, solution = generate_quadratic_equation()
                else:
                    equation, hints, solution = generate_cubic_equation()
                # else:
                #     equation, hints, solution = generate_simultaneous_equation()
                
                file.write(f"{equation_type}\t{equation}\t{hints}\t{solution}\n")  # Write equation, hints, and solution to file

# Generate file of equations on requested amount (make sure nama parent folder is the same, kalau tak dia akan keluar error)
generate_equation_file('equations.tsv', 10)