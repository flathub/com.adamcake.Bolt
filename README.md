# bolt-flatpak
Flathub repo for [Bolt Launcher](https://github.com/Adamcake/Bolt/). See there for more details on what this software does, how to use it, who made it and why, and so on.

## install
`flatpak install com.adamcake.Bolt`

## build
`flatpak-builder --user --install --install-deps-from=flathub --force-clean build-dir com.adamcake.Bolt.yml`

## maintenance
If changing anything about the CEF module, make sure the various git modules that get checked out all have their commit hashes updated as appropriate. There may be some new ones or some that are no longer necessary, especially if updating Chromium 118 or later, in which case most of its submodules are now in its .gitmodules and will be checked out automatically. `gn-fix-building-in-flathub.patch` adds mostly hard-coded stuff which will need to be updated for the new checkout as well.
