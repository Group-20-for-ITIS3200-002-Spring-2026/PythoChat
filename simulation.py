import text_encryption

def simulate_mitm_attack():
    print(" --- MITM SIMULATION ---\n")

    p = 23
    g = 5

    # Private keys
    alice_private = 6
    bob_private = 15
    mallory_private = 13

    # Generating Public keys
    alice_public = text_encryption.generate_public_key(alice_private, g, p)
    bob_public = text_encryption.generate_public_key(bob_private, g, p)
    mallory_public = text_encryption.generate_public_key(mallory_private, g, p)

    print("Mallory is intercepting the connection...\n")

    # Mallory swaps keys
    alice_shared = text_encryption.generate_shared_key(mallory_public, alice_private, p)
    bob_shared = text_encryption.generate_shared_key(mallory_public, bob_private, p)

    mallory_shared_with_alice = text_encryption.generate_shared_key(alice_public, mallory_private, p)
    mallory_shared_with_bob = text_encryption.generate_shared_key(bob_public, mallory_private, p)

    # Derive AES keys, so they can be used for encryption
    alice_key = text_encryption.derive_key(alice_shared)
    bob_key = text_encryption.derive_key(bob_shared)
    mallory_key_alice = text_encryption.derive_key(mallory_shared_with_alice)
    mallory_key_bob = text_encryption.derive_key(mallory_shared_with_bob)

    print("Compromised Connection established \n")

    while True:
        msg_alice = input("Alice: ")
        if msg_alice.lower() == "exit":
            print("Chat ended.")
            break

        C, H = text_encryption.encrypt_text(msg_alice, alice_key)
        print("\nEncrypted message sent to Bob")

        #  Mallory intercepts the text
        intercepted = text_encryption.decrypt_text(C, H, mallory_key_alice)

        print(f"Mallory sees: {intercepted}")

        # Mallory edits message
        edited = input("Mallory edit message (press enter to keep same): ")
        if edited.strip() == "":
            edited = intercepted

        print(f"Mallory forwards: {edited}\n")

        # Re-encrypt for Bob
        C2, H2 = text_encryption.encrypt_text(edited, mallory_key_bob)

        # Bob recives
        bob_msg = text_encryption.decrypt_text(C2, H2, bob_key)

        if bob_msg:
            print(f"Bob received: {bob_msg}")
        else:
            print("Bob: Message verification failed!")
            continue

        # Bob replies 
        msg_bob = input("\nBob: ")
        if msg_bob.lower() == "exit":
            print("Chat ended.")
            break

        C, H = text_encryption.encrypt_text(msg_bob, bob_key)
        print("\n[Encrypted reply sent to Alice]")

        # Mallory intercepts the text
        intercepted = text_encryption.decrypt_text(C, H, mallory_key_bob)

        print(f"Mallory sees: {intercepted}")

        # Mallory edits reply
        edited = input("Mallory edit reply (press enter to keep same): ")
        if edited.strip() == "":
            edited = intercepted

        print(f"Mallory forwards: {edited}\n")

        # Re-encrypt for Alice
        C2, H2 = text_encryption.encrypt_text(edited, mallory_key_alice)

        # Alice receives 
        alice_msg = text_encryption.decrypt_text(C2, H2, alice_key)

        if alice_msg:
            print(f"Alice received: {alice_msg}\n")
        else:
            print("Alice: Message verification failed!\n")


if __name__ == "__main__":
    simulate_mitm_attack()
