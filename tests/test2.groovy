def cmd = "curl -u $username:$password https://api.example.com"
def process = cmd.execute()
println process.text