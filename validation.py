# Assuming token_validation is already defined

# Function you want to wrap with token validation
@token_validation
def my_protected_function(token, data):
    # This function will only run if the token validation succeeds
    return {
        "status": "success",
        "data": data
    }

# Example usage
example_token = "your_jwt_token_here"

result = my_protected_function(example_token, {"key": "value"})

print(result)
