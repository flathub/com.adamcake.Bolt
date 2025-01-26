# bolt-flatpak
Flathub repo for [Bolt Launcher](https://github.com/Adamcake/Bolt/). See there for more details on what this software does, how to use it, who made it and why, and so on.

If you're reading this repo to try to work out how to build Bolt in your own build system or package manager, I strongly suggest referencing a different one, such as AUR's `bolt-launcher`, to make your life much simpler. If you insist on continuing here, then be aware that almost everything you're reading is the configuration for a custom source-build of Chromium and CEF within flatpak's build system, which you probably don't care about. When reading `com.adamcake.Bolt.yml`, you can ignore the entire "chromium" module - which takes up most of the file - and skip to the "bolt" module at the end for the useful part.

## install
`flatpak install com.adamcake.Bolt`

## build
`flatpak-builder --user --install --install-deps-from=flathub --force-clean build-dir com.adamcake.Bolt.yml`

## maintenance
If changing the checkout version of the Chromium or CEF modules, all of the following need to be done:
- `gn-fix-building-in-flathub.patch` adds mostly hard-coded stuff which will need to be updated for the new checkouts.
- `chromium-dont-update-rust.patch` also adds a hard-coded string which will need to be updated if the rust toolchain is changed.
- all submodules will need to have their specific commit updated to match the new version, and the relevant patch lists in `com.adamcake.Bolt.yml` need updating to match.
- ungoogled-chromium checkout commit must be updated to match the chromium version.
- generate-node-sources.py should be given the package-lock.json that is located in chromium at <root>/third_party/node/package-lock.json on the version you are trying to build. This will create the third-party-node-modules.yml that you can check into the source control for subsequent builds.
- generate-submodule-sources.py should be given the root of your chromium build directory, which contains the .gitmodules file. This will create chromium-submodules.yaml.
- `chromium-submodules.yaml` needs to be updated according to the `.gitmodules` from the chromium revision you're building.
