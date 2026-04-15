# OwlSafe (WIP)

## Compile
### Clone Repo
```
git clone https://github.com/OwlWorksInnovations/OwlSafe.git
```

### Development
```
wails dev
```

### Build
```
wails build
```
then open executable in build/bin

## NOTICE
Instead of keeping all my files inside the backend folder I am just developing them there until they are ready to go to my monorepo with all my go packages. This way I can easily reuse my code in all my projects so if can't find code you want to modify look at my go-packages repo and then simply throw them into the project and change the imports. I have built them in such a way that they should be able to work in any project; not all packages are finished and I don't plan on maintaining them for anyone except myself.
