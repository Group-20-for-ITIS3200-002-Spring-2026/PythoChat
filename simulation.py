import text_encryption

def simulate_text_messaging():
    print(" --- TEXT MESSAGE SIMULATION ---\n")

    p = 23
    g = 5

    alice_private = 6
    bob_private = 15

    #keys creation
    alice_public = text_encryption.generate_public_key(alice_private, g, p)
    bob_public = text_encryption.generate_public_key(bob_private, g, p)

    print(f"Alice Public Key: {alice_public}")
    print(f"Bob Public Key: {bob_public}\n")

    
    alice_shared = text_encryption.generate_shared_key(bob_public, alice_private, p)
    bob_shared = text_encryption.generate_shared_key(alice_public, bob_private, p)

    print(f"Alice Shared Key: {alice_shared}")
    print(f"Bob Shared Key: {bob_shared}\n")

    
    alice_key = text_encryption.derive_key(alice_shared)
    bob_key = text_encryption.derive_key(bob_shared)

    # Loop that runs till one user sends exit.
    while True:
        # ===== Alice sends =====
        msg_alice = input("Alice: ")
        if msg_alice.lower() == "exit":
            print("Chat ended.")
            break

        C, H = text_encryption.encrypt_text(msg_alice, alice_key)
        print("\nEncrypted message sent to Bob")

        print(f"Ciphertext (C): {C.hex()}")
        print(f"Hash (H): {H.hex()}\n")

        # Bob receives
        bob_msg = text_encryption.decrypt_text(C, H, bob_key)

        if bob_msg:
            print(f"Bob received: {bob_msg}")
        else:
            print("Bob: Message verification failed!")
            continue

        # ===== Bob replies =====
        msg_bob = input("\nBob: ")
        if msg_bob.lower() == "exit":
            print("Chat ended.")
            break

        C, H = text_encryption.encrypt_text(msg_bob, bob_key)
        print("\nEncrypted reply sent to Alice")

        print(f"Ciphertext (C): {C.hex()}")
        print(f"Hash (H): {H.hex()}\n")

        # Alice receives
        alice_msg = text_encryption.decrypt_text(C, H, alice_key)

        if alice_msg:
            print(f"Alice received: {alice_msg}\n")
        else:
            print("Alice: Message verification failed!\n")


if __name__ == "__main__":
    simulate_text_messaging()
