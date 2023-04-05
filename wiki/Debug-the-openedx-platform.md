
### Debug the platform

To debug a local edx-platform repository, add a `import ipdb; ipdb.set_trace()` breakpoint anywhere in your code and run:

`tutor dev runserver -v /path/to/edx-platform:/openedx/edx-platform lms`

Referance link -> https://docs.tutor.overhang.io/dev.html#debug-edx-platform

