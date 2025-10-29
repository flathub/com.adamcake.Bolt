#!/bin/bash

set -xeuo pipefail

patch -p1 --directory=third_party/node < third_party/node/patches/lit_html.patch
patch -p1 --directory=third_party/node < third_party/node/patches/typescript.patch
patch -p1 --directory=third_party/node/node_modules/@types/d3 < third_party/node/patches/chromium_d3_types_index.patch
patch -p1 --directory=third_party/node < third_party/node/patches/types_chai.patch
patch -p1 --directory=third_party/node < third_party/node/patches/ts_poet.patch
patch -p1 --directory=third_party/node < third_party/node/patches/types_trusted_types.patch

./build/util/lastchange.py -m SKIA_COMMIT_HASH -s third_party/skia --header skia/ext/skia_commit_hash.h
/usr/bin/env CC=gcc CXX=g++ python3 gn/build/gen.py
/usr/bin/env CC=gcc CXX=g++ ninja -C gn/out -j $FLATPAK_BUILDER_N_JOBS

# symlink llvm for chromium to use
mkdir -p third_party/llvm-build
ln -s /app/lib/sdk/llvm21 $FLATPAK_BUILDER_BUILDDIR/third_party/llvm-build/Release+Asserts

#https://github.com/flathub/io.github.ungoogled_software.ungoogled_chromium/blob/3673d6bfd7d8947bd0736e49cdc8c738d0f07bfb/build-aux/build.sh#L55
mkdir -p bindgen/bin
ln -svf "$(command -v bindgen)" bindgen/bin/bindgen
ln -svf "${LIBCLANG_PATH}" -t bindgen

export GN_DEFINES="$GN_DEFINES rust_bindgen_root=$FLATPAK_BUILDER_BUILDDIR/bindgen \
	rustc_version=\"$(rustc --version)\" \
	rust_sysroot_absolute=$(rustc --print sysroot) \
	clang_base_path=$(llvm-config --prefix) \
	clang_version=$(llvm-config --version | awk -F. '{print $1}')"

/usr/bin/env python3 cef/tools/gclient_hook.py

# From ungoogled chromium flatpak
patch -p1 < flatpak-Adjust-paths-for-the-sandbox.patch
patch -p1 --directory=third_party/angle < angle-remove-undefined-const.patch
patch -p1 --directory=ungoogled-chromium < ungoogled-chromium-adjust-for-cef.patch
patch -p1 --directory=ungoogled-chromium < ungoogled-chromium-ignore-nonexistent-binaries.patch
patch -p1 --directory=ungoogled-chromium < ungoogled-chromium-remove-extra-locales.patch

./ungoogled-chromium/utils/prune_binaries.py . ungoogled-chromium/pruning.list
./ungoogled-chromium/utils/patches.py apply . ungoogled-chromium/patches
./ungoogled-chromium/utils/domain_substitution.py apply -r ungoogled-chromium/domain_regex.list -f ungoogled-chromium/domain_substitution.list -c domsubcache.tar.gz .

#Use system node
mkdir -p third_party/node/linux/node-linux-x64/bin
ln -sfn /usr/lib/sdk/node22/bin/node third_party/node/linux/node-linux-x64/bin/node

/usr/bin/env ninja -k 0 -C out/Release_GN -j $FLATPAK_BUILDER_N_JOBS libcef chrome_sandbox || /usr/bin/env ninja -C out/Release_GN -j $FLATPAK_BUILDER_N_JOBS libcef chrome_sandbox
python3 ./cef/tools/make_distrib.py --ninja-build --minimal --no-docs --no-archive --output-dir=/app/cef
