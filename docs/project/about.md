# About

muru-hosting is a proof of concept by Graham Dumpleton, the author of
[Muru](https://github.com/muruhq/muru). Its purpose is Muru's:

- to dogfood Muru with a real application that uses all three of its ways
  of running: `muructl serve` for the control plane and the helper in
  each site's pod, and the Muru daemon for every hosted site;

- to test Muru's admin API against what a hosting service needs, filing
  each gap as an issue against Muru;

- to work out, with something running, how Muru should change to suit
  web hosting services for Python applications, such as keeping its
  controller and edge out of reach of the code they host.

It is not a product. It makes no promise of stability, may change
completely or stop, and is not going to become a supported project that
others can run for themselves.

Like Muru, it is developed with extensive use of AI coding agents,
directed and reviewed by its creator.
