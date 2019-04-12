/**
 * This file is part of Shuup Admin Channel.
 *
 * Copyright (c) 2019, Christian Hess. All rights reserved.
 *
 * This source code is licensed under the MIT license found in the
 * LICENSE file in the root directory of this source tree.
 */
const { getParcelBuildCommand, runBuildCommands } = require("shuup-static-build-tools");

runBuildCommands([
    getParcelBuildCommand({
        cacheDir: "shuup-admin-channel",
        entryFile: "static_src/shuup-admin-channel.js"
    })
]);
