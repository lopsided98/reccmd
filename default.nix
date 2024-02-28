{ lib, runCommand, python3, linkFarm }: let
    self = runCommand "reccmd" {
        buildInputs = [ python3 ];

        passthru = {
            inherit asCommands;
        };
    } ''
        mkdir -p "$out"/bin
        cp '${./reccmd.py}' "$out"/bin/reccmd
        patchShebangs "$out"/bin
    '';

    asCommands = cmds: linkFarm "reccmd-play" (builtins.map (cmd: {
        name = "bin/${cmd}";
        path = "${self}/bin/reccmd";
    }) cmds);
in self