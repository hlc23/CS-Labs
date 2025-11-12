# CS-Labs
Labs/Demo for cyber security.  
For educational purposes only.

## Requirements  
- docker-compose

## How to Use  
### Cloning the Repository  
```bash
git clone https://github.com/hlc23/CS-Labs.git
cd CS-Labs
cd XXX # replace XXX with the lab you want to run
docker-compose up -d # run the lab
```
### Download individual lab  
Download from `build` folder  
Unzip the file and run `docker-compose up -d` inside the unzipped folder.

## Lab List
- [csrf-demo](./CSRF-demo/): A demo of CSRF.
- [SameSite-cookie](./SameSite-cookie/): Show differences of SameSite cookie settings (Lax, Strict, None).

