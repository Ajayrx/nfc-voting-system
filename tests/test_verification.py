from main.voter_verification import verify_voter

print("🔁 Running 5 Verification Simulations:\n")
for i in range(5):
    print(f"🧪 Test #{i+1}")
    verify_voter()
