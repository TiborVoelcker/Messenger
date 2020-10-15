# Messenger
A (badly) encrypted messenger for two parties. Just a project for learning purposes.

---

**!DISCLAIMER: This app uses a handwritten key exchange algorithm (Diffie-Hellman) which almost certainly has MAJOR flaws and is therefore not secure. Do not use!**
Although I do not really think that that is a real concern, I still think it is necessary to be said.

A server script to run on a machine, together with a client script where two people can then chat with eachother when typing the IP of the server. Only two people are allowed on the server because I was too lazy to implement the key exchange for more than two parties. It uses sockets for the communication, PyQt5 for the GUI, Diffie-Hellman for the key exchange and a (not handwritten) Blowfish algorithm for the encryption. 
### Main takeaways
- how Server-Client communication works (with sockets)
- how encryption works
- that encryption should be left for the experts
