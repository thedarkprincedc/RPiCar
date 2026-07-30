## Secure Shell Access
### Generate SSH Key

Create Key (Default)
```bash 
ssh-keygen -t ed25519 -C "your_email@example.com"
```

Create Key (Custom)
```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_rpicar -C "Raspberry Pi"
```

Copy SSH Key to Server
```bash
ssh-copy-id admin@<pi-ip-address>
```

Copy SSH Key to Server (With ID)
```bash
ssh-copy-id -i ~/.ssh/id_ed25519_rpicar.pub admin@<pi-ip-address>
```

Login (Default)
```bash
ssh admin@<pi-ip-address>
```

Login (With Key)
```bash
ssh -i ~/.ssh/my_key admin@<pi-ip-address>
```
