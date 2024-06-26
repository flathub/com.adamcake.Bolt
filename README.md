# bolt-flatpak
Flathub repo for [Bolt Launcher](https://github.com/Adamcake/Bolt/). See there for more details on what this software does, how to use it, who made it and why, and so on.

## install
`flatpak install com.adamcake.Bolt`

## build
`flatpak-builder --user --install --install-deps-from=flathub --force-clean build-dir com.adamcake.Bolt.yml`

## maintenance
**Note**: as of 0.9 we've reverted to downloading pre-built CEF binaries instead of building them from source, so most of this section doesn't apply anymore. We had to revert to work around flatpak-builder bug #599 which doesn't look like it's getting fixed any time soon. If it does, we'll go back to the source builds.

If changing the checkout version of the Chromium or CEF modules, all of the following need to be done:
- make sure the various git modules that get checked out all have their commit hashes updated as appropriate. There may be some new ones or some that are no longer necessary, especially if updating Chromium 118 or later, in which case most of its submodules are now in its .gitmodules and will be checked out automatically.
- `gn-fix-building-in-flathub.patch` adds mostly hard-coded stuff which will need to be updated for the new checkouts.
- all submodules will need to have their specific commit updated to match the new version. Submodules with chromium patches in them will therefore need to have their patch list updated in `com.adamcake.Bolt.yml`.
- ungoogled-chromium checkout commit must be updated to match the chromium version.
- generate-sources.py should be given the package-lock.json that is located in chromium at <root>/third_party/node/package-lock.json on the version you are trying to build. This will create the third-party-node-modules.yml that you can check into the source control for subsequent builds.
