{ lib, runCommand, linkFarm }: let
    self = runCommand "reccmd" {
        passthru = {
            inherit asCommands;
        };
    } ''
        mkdir -p "$out"/bin
        cp '${./reccmd.py}' "$out/bin/reccmd"
    '';

    asCommands = cmds: linkFarm (lib.map (cmd: {
        name = "bin/cmd";
        path = "${self}/bin/reccmd";
    }) cmds);
in self