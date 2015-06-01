from i3pystatus.core.command import run_through_shell

from i3pystatus.updates import Backend


class Pacman(Backend):
    """
    Checks for updates in Arch Linux pacman repositories using the
    `checkupdates` script.
    """

    @property
    def updates(self):
        command = ["checkupdates"]
        checkupdates = run_through_shell(command)
        out = checkupdates.out.strip()

        return len(out.split("\n")) if len(out) > 0 else 0

Backend = Pacman
