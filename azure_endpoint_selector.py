#!/usr/bin/env python3
"""
Azure Network Endpoint Decision Tree Tool

Interactive CLI tool that guides users through selecting the appropriate
Azure network endpoint based on their application requirements.

Based on Microsoft Azure networking best practices.
"""

import sys
import time
from typing import Optional


# ═══════════════════════════════════════════════════════════════════════════════
# AZURE THEME - Terminal Colors and Styling
# ═══════════════════════════════════════════════════════════════════════════════

class AzureTheme:
    """Azure-themed terminal colors and ASCII components."""

    # Blues - gradient for animations
    AZURE_BLUE = "\033[38;5;39m"       # Bright Azure Blue
    AZURE_DARK = "\033[38;5;24m"       # Deep Azure
    AZURE_LIGHT = "\033[38;5;117m"     # Light Sky Blue
    AZURE_ACCENT = "\033[38;5;33m"     # Core Azure
    AZURE_GLOW = "\033[38;5;81m"       # Cyan glow
    AZURE_DEEP = "\033[38;5;27m"       # Deep blue

    # Greys
    GREY_DARK = "\033[38;5;236m"       # Charcoal
    GREY_MID = "\033[38;5;245m"        # Steel Grey
    GREY_LIGHT = "\033[38;5;250m"      # Silver
    GREY_SUBTLE = "\033[38;5;240m"     # Dim Grey

    # Utility
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RESET = "\033[0m"
    CLEAR_LINE = "\033[2K"
    CURSOR_UP = "\033[A"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

    # Logo lines without box
    LOGO_LINES = [
        " █████╗ ███████╗██╗   ██╗██████╗ ███████╗",
        "██╔══██╗╚══███╔╝██║   ██║██╔══██╗██╔════╝",
        "███████║  ███╔╝ ██║   ██║██████╔╝█████╗  ",
        "██╔══██║ ███╔╝  ██║   ██║██╔══██╗██╔══╝  ",
        "██║  ██║███████╗╚██████╔╝██║  ██║███████╗",
        "╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝",
    ]

    @classmethod
    def animate_logo(cls, title: str, subtitle: str = ""):
        """Animate the logo with a sweep effect."""
        print(cls.HIDE_CURSOR, end="")
        sys.stdout.flush()

        colors = [cls.AZURE_DEEP, cls.AZURE_DARK, cls.AZURE_ACCENT, cls.AZURE_BLUE, cls.AZURE_LIGHT, cls.AZURE_GLOW]
        print()

        # Reveal animation - line by line with color sweep
        for line in cls.LOGO_LINES:
            # Quick color sweep across each line
            for color_idx in range(len(colors)):
                print(f"\r  {colors[color_idx]}{line}{cls.RESET}", end="")
                sys.stdout.flush()
                time.sleep(0.02)
            print()
            time.sleep(0.05)

        # Pulse effect - cycle through colors on full logo
        for pulse in range(2):
            for color in colors:
                # Move cursor up to redraw
                print(f"\033[{len(cls.LOGO_LINES)}A", end="")
                for line in cls.LOGO_LINES:
                    print(f"\r  {color}{line}{cls.RESET}")
                sys.stdout.flush()
                time.sleep(0.04)

        # Final state with glow
        print(f"\033[{len(cls.LOGO_LINES)}A", end="")
        for line in cls.LOGO_LINES:
            print(f"\r  {cls.AZURE_LIGHT}{line}{cls.RESET}")

        # Animated underline
        print()
        underline = "═" * 44
        for i in range(len(underline) + 1):
            print(f"\r  {cls.AZURE_BLUE}{underline[:i]}{cls.RESET}", end="")
            sys.stdout.flush()
            time.sleep(0.008)
        print()

        # Title with typewriter effect
        print()
        title_text = f"  {cls.GREY_LIGHT}◆ {cls.BOLD}{title}{cls.RESET}"
        for i in range(len(title) + 5):
            print(f"\r  {cls.GREY_LIGHT}◆ {cls.BOLD}{title[:max(0, i-4)]}{cls.RESET}", end="")
            sys.stdout.flush()
            time.sleep(0.015)
        print()

        if subtitle:
            for i in range(len(subtitle) + 1):
                print(f"\r    {cls.GREY_MID}{subtitle[:i]}{cls.RESET}", end="")
                sys.stdout.flush()
                time.sleep(0.01)
            print()

        print(cls.SHOW_CURSOR, end="")
        sys.stdout.flush()
        print()

    @classmethod
    def header(cls, title: str, subtitle: str = "") -> str:
        """Generate themed header (static version)."""
        lines = [
            "",
        ]
        for line in cls.LOGO_LINES:
            lines.append(f"  {cls.AZURE_LIGHT}{line}{cls.RESET}")
        lines.extend([
            f"  {cls.AZURE_BLUE}{'═' * 44}{cls.RESET}",
            "",
            f"  {cls.GREY_LIGHT}◆ {cls.BOLD}{title}{cls.RESET}",
            f"    {cls.GREY_MID}{subtitle}{cls.RESET}" if subtitle else "",
            "",
        ])
        return "\n".join(line for line in lines if line is not None and line != "")

    @classmethod
    def section(cls, title: str) -> str:
        """Generate section divider."""
        return f"\n{cls.AZURE_ACCENT}━━━ {cls.BOLD}{title}{cls.RESET} {cls.AZURE_ACCENT}━━━{cls.RESET}\n"

    @classmethod
    def question_box(cls, question: str, context: Optional[str] = None) -> str:
        """Generate a compact question prompt."""
        if context:
            return f"{cls.AZURE_LIGHT}?{cls.RESET} {cls.BOLD}{question}{cls.RESET} {cls.GREY_MID}({context}){cls.RESET}"
        return f"{cls.AZURE_LIGHT}?{cls.RESET} {cls.BOLD}{question}{cls.RESET}"

    @classmethod
    def option(cls, num: int, key: str, description: str) -> str:
        """Format a menu option (compact inline style)."""
        return f"{cls.AZURE_BLUE}[{num}]{cls.RESET} {cls.GREY_LIGHT}{key}{cls.RESET}"

    @classmethod
    def options_inline(cls, options: list[tuple[str, str]]) -> str:
        """Format options inline."""
        parts = []
        for i, (key, desc) in enumerate(options, 1):
            parts.append(f"{cls.AZURE_BLUE}[{i}]{cls.RESET} {cls.GREY_LIGHT}{key}{cls.RESET}")
        return "  " + "  ".join(parts)

    @classmethod
    def prompt(cls, text: str) -> str:
        """Format input prompt."""
        return f"  {cls.AZURE_ACCENT}▸{cls.RESET} {text}"

    @classmethod
    def success(cls, text: str) -> str:
        """Format success message."""
        return f"{cls.AZURE_BLUE}[✓]{cls.RESET} {text}"

    @classmethod
    def info(cls, text: str) -> str:
        """Format info line."""
        return f"{cls.GREY_LIGHT}│{cls.RESET} {text}"

    @classmethod
    def bullet(cls, text: str) -> str:
        """Format bullet point."""
        return f"    {cls.AZURE_LIGHT}•{cls.RESET} {cls.GREY_LIGHT}{text}{cls.RESET}"

    @classmethod
    def animate_result(cls, title: str, content_lines: list):
        """Animate the result display."""
        width = 64
        print(cls.HIDE_CURSOR, end="")
        sys.stdout.flush()

        # Animated border reveal
        print()
        for i in range(width + 1):
            print(f"\r{cls.AZURE_BLUE}╔{'═' * i}{cls.RESET}", end="")
            sys.stdout.flush()
            time.sleep(0.005)
        print(f"{cls.AZURE_BLUE}╗{cls.RESET}")

        # Title with checkmark animation
        print(f"{cls.AZURE_BLUE}║{cls.RESET}  ", end="")
        time.sleep(0.1)
        # Spinner then checkmark
        spinners = ["◐", "◓", "◑", "◒", "◐", "◓", "✓"]
        for s in spinners:
            print(f"\r{cls.AZURE_BLUE}║{cls.RESET}  {cls.AZURE_LIGHT}{s}{cls.RESET}", end="")
            sys.stdout.flush()
            time.sleep(0.08)
        print(f" {cls.BOLD}{title}{cls.RESET}")

        # Divider
        for i in range(width + 1):
            print(f"\r{cls.AZURE_BLUE}╠{'═' * i}{cls.RESET}", end="")
            sys.stdout.flush()
            time.sleep(0.003)
        print(f"{cls.AZURE_BLUE}╣{cls.RESET}")

        # Content lines with fade-in effect
        for line in content_lines:
            print(f"{cls.AZURE_BLUE}║{cls.RESET}  {line}")
            time.sleep(0.03)

        # Bottom border
        for i in range(width + 1):
            print(f"\r{cls.AZURE_BLUE}╚{'═' * i}{cls.RESET}", end="")
            sys.stdout.flush()
            time.sleep(0.003)
        print(f"{cls.AZURE_BLUE}╝{cls.RESET}")
        print()

        print(cls.SHOW_CURSOR, end="")
        sys.stdout.flush()

    @classmethod
    def result_box(cls, title: str, content_lines: list) -> str:
        """Generate a result box with content (static version)."""
        width = 64
        lines = [
            "",
            f"{cls.AZURE_BLUE}╔{'═' * width}╗{cls.RESET}",
            f"{cls.AZURE_BLUE}║{cls.RESET}  {cls.AZURE_LIGHT}✓{cls.RESET} {cls.BOLD}{title}{cls.RESET}",
            f"{cls.AZURE_BLUE}╠{'═' * width}╣{cls.RESET}",
        ]
        for line in content_lines:
            lines.append(f"{cls.AZURE_BLUE}║{cls.RESET}  {line}")
        lines.append(f"{cls.AZURE_BLUE}╚{'═' * width}╝{cls.RESET}")
        lines.append("")
        return "\n".join(lines)

    @classmethod
    def divider(cls, style: str = "light") -> str:
        """Generate a divider line."""
        if style == "heavy":
            return f"{cls.AZURE_DARK}{'━' * 64}{cls.RESET}"
        elif style == "double":
            return f"{cls.AZURE_BLUE}{'═' * 64}{cls.RESET}"
        else:
            return f"{cls.GREY_SUBTLE}{'─' * 64}{cls.RESET}"

    @classmethod
    def footer(cls) -> str:
        """Generate themed footer."""
        return f"\n{cls.GREY_SUBTLE}░░░ {cls.GREY_MID}Azure Network Endpoint Selector{cls.RESET} {cls.GREY_SUBTLE}░░░{cls.RESET}\n"


# ═══════════════════════════════════════════════════════════════════════════════
# AZURE ENDPOINT SELECTOR
# ═══════════════════════════════════════════════════════════════════════════════

class AzureEndpointSelector:
    """Decision tree for selecting Azure network endpoints."""

    ENDPOINTS = {
        "azure_load_balancer": {
            "name": "Azure Load Balancer",
            "description": "Layer 4 (TCP/UDP) load balancer for non-HTTP workloads.",
            "use_cases": [
                "Internal or external TCP/UDP traffic distribution",
                "High availability for VMs and scale sets",
                "Non-web applications (databases, custom protocols)",
            ],
            "waf_pillar": "Reliability, Performance Efficiency",
        },
        "application_gateway": {
            "name": "Application Gateway",
            "description": "Layer 7 (HTTP/HTTPS) load balancer with WAF capabilities.",
            "use_cases": [
                "Web applications requiring SSL termination",
                "URL-based routing",
                "Session affinity",
                "Web Application Firewall (WAF)",
            ],
            "waf_pillar": "Security, Reliability",
        },
        "traffic_manager_alb": {
            "name": "Traffic Manager + Azure Load Balancer",
            "description": "DNS-based global traffic distribution with regional load balancing.",
            "use_cases": [
                "Multi-region non-HTTP deployments",
                "DNS-level failover for TCP/UDP workloads",
                "Geographic routing for non-web apps",
            ],
            "waf_pillar": "Reliability, Performance Efficiency",
        },
        "front_door": {
            "name": "Azure Front Door",
            "description": "Global HTTP/HTTPS load balancer with CDN and WAF.",
            "use_cases": [
                "Global web applications (PaaS)",
                "Performance acceleration via edge locations",
                "Global WAF protection",
                "SSL offloading at the edge",
            ],
            "waf_pillar": "Performance Efficiency, Security",
        },
        "front_door_app_gateway": {
            "name": "Azure Front Door + Application Gateway",
            "description": "Global entry point with regional Layer 7 processing.",
            "use_cases": [
                "Global apps requiring per-request app-layer processing",
                "AKS with ingress controller",
                "Complex routing with regional WAF policies",
            ],
            "waf_pillar": "Security, Performance Efficiency, Reliability",
        },
        "front_door_alb": {
            "name": "Azure Front Door + Azure Load Balancer",
            "description": "Global HTTP entry with regional Layer 4 distribution.",
            "use_cases": [
                "IaaS (VM-based) global web deployments",
                "VMs behind load balancer with global front end",
            ],
            "waf_pillar": "Performance Efficiency, Reliability",
        },
        "front_door_app_gateway_ingress": {
            "name": "Azure Front Door + Application Gateway + Ingress Controller",
            "description": "Full stack for AKS with global distribution.",
            "use_cases": [
                "AKS clusters requiring global load balancing",
                "Kubernetes ingress with Azure-native integration",
                "Multi-cluster AKS deployments",
            ],
            "waf_pillar": "Reliability, Security, Operational Excellence",
        },
    }

    def __init__(self):
        self.answers = {}
        self.theme = AzureTheme

    def ask_yes_no(self, question: str, context: Optional[str] = None) -> bool:
        """Prompt user with a yes/no question (compact single-line)."""
        prompt_text = self.theme.question_box(question, context)
        while True:
            response = input(f"{prompt_text} {self.theme.AZURE_ACCENT}[y/n]{self.theme.RESET} ").strip().lower()
            if response in ("y", "yes"):
                return True
            elif response in ("n", "no"):
                return False
            print(f"  {self.theme.GREY_MID}Enter 'y' or 'n'{self.theme.RESET}")

    def ask_choice(self, question: str, options: list[tuple[str, str]]) -> str:
        """Prompt user with multiple choice question (compact)."""
        print(self.theme.question_box(question))
        print(self.theme.options_inline(options))
        while True:
            try:
                response = int(input(f"  {self.theme.AZURE_ACCENT}▸{self.theme.RESET} ").strip())
                if 1 <= response <= len(options):
                    return options[response - 1][0]
            except ValueError:
                pass
            print(f"  {self.theme.GREY_MID}Enter 1-{len(options)}{self.theme.RESET}")

    def display_result(self, endpoint_key: str):
        """Display the recommended endpoint with details (animated)."""
        endpoint = self.ENDPOINTS[endpoint_key]

        content_lines = [
            "",
            f"{self.theme.AZURE_ACCENT}{self.theme.BOLD}{endpoint['name']}{self.theme.RESET}",
            "",
            f"{self.theme.GREY_LIGHT}{endpoint['description']}{self.theme.RESET}",
            "",
            f"{self.theme.GREY_MID}Use Cases:{self.theme.RESET}",
        ]

        for use_case in endpoint["use_cases"]:
            content_lines.append(f"  {self.theme.AZURE_LIGHT}•{self.theme.RESET} {self.theme.GREY_LIGHT}{use_case}{self.theme.RESET}")

        content_lines.extend([
            "",
            f"{self.theme.GREY_MID}WAF Pillars:{self.theme.RESET} {self.theme.AZURE_LIGHT}{endpoint['waf_pillar']}{self.theme.RESET}",
            "",
        ])

        print()
        self.theme.animate_result("RECOMMENDED AZURE NETWORK ENDPOINT", content_lines)

    def run_decision_tree(self) -> str:
        """Execute the decision tree and return the recommended endpoint."""

        self.theme.animate_logo(
            "NETWORK ENDPOINT SELECTOR",
            "Based on Azure Well-Architected Framework"
        )

        # Question 1: Web app?
        is_web_app = self.ask_yes_no(
            "Is this a web application?",
            "HTTP/HTTPS traffic"
        )
        self.answers["is_web_app"] = is_web_app

        if not is_web_app:
            # Non-web application path
            is_internet_facing = self.ask_yes_no(
                "Is the application internet-facing?",
                "Accessible from the public internet"
            )
            self.answers["is_internet_facing"] = is_internet_facing

            if not is_internet_facing:
                return "azure_load_balancer"

            # Internet-facing non-web app
            is_global = self.ask_yes_no(
                "Is this a global deployment across multiple regions?",
                "Deployed in 2+ Azure regions"
            )
            self.answers["is_global"] = is_global

            if is_global:
                return "traffic_manager_alb"
            else:
                return "application_gateway"

        # Web application path
        is_internet_facing = self.ask_yes_no(
            "Is the application internet-facing?",
            "Accessible from the public internet"
        )
        self.answers["is_internet_facing"] = is_internet_facing

        if not is_internet_facing:
            return "application_gateway"

        # Internet-facing web app
        is_global = self.ask_yes_no(
            "Is this a global deployment across multiple regions?",
            "Deployed in 2+ Azure regions"
        )
        self.answers["is_global"] = is_global

        if not is_global:
            # Single region web app
            needs_acceleration = self.ask_yes_no(
                "Do you require performance acceleration?",
                "CDN, edge caching, global anycast"
            )
            self.answers["needs_acceleration"] = needs_acceleration

            if not needs_acceleration:
                return "application_gateway"
            # If needs acceleration, continue to hosting question below

        # Global or needs acceleration - check SSL/app-layer requirements
        if is_global:
            needs_ssl_offload = self.ask_yes_no(
                "Do you require SSL offloading or app-layer processing per request?",
                "URL rewriting, header manipulation, path-based routing at regional level"
            )
            self.answers["needs_ssl_offload"] = needs_ssl_offload

            if needs_ssl_offload:
                return "front_door_app_gateway"

        # Check hosting model
        hosting = self.ask_choice(
            "What is your hosting model?",
            [
                ("PaaS", "App Service, Functions, Container Apps"),
                ("AKS", "Azure Kubernetes Service"),
                ("IaaS", "Virtual Machines, VM Scale Sets"),
            ]
        )
        self.answers["hosting"] = hosting

        if hosting == "PaaS":
            return "front_door"
        elif hosting == "AKS":
            return "front_door_app_gateway_ingress"
        else:  # IaaS
            return "front_door_alb"

    def run(self):
        """Main entry point."""
        try:
            result = self.run_decision_tree()
            self.display_result(result)

            print(self.theme.section("Your Responses"))
            for key, value in self.answers.items():
                display_key = key.replace("_", " ").title()
                print(self.theme.bullet(f"{display_key}: {value}"))

            print(self.theme.footer())

        except KeyboardInterrupt:
            print(f"\n\n  {self.theme.GREY_MID}Cancelled by user.{self.theme.RESET}")
            sys.exit(0)


def main():
    selector = AzureEndpointSelector()
    selector.run()


if __name__ == "__main__":
    main()
