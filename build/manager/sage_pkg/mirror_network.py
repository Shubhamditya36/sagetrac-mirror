"""
Download files from the Sage mirror network
"""

#*****************************************************************************
#  Copyright (C) 2014  Volker Braun <vbraun.name@gmail.com>
#  Distributed under the terms of the GNU General Public License (GPL)
#  as published by the Free Software Foundation; either version 2 of
#  the License, or (at your option) any later version.
#                  http://www.gnu.org/licenses/
#*****************************************************************************

import contextlib
import os
import sys

try:
    # Python 3
    import urllib.request as urllib
    import urllib.parse as urlparse
except ImportError:
    import urllib
    import urlparse

from sage_pkg.config import config


def http_error_default(url, fp, errcode, errmsg, headers):
    """
    Callback for the URLopener to raise an exception on HTTP errors
    """
    fp.close()
    raise IOError(errcode, errmsg, url)


class ProgressBar(object):
    """
    Progress bar as urllib reporthook
    """

    def __init__(self, length=60):
        self.length = length
        self.progress = 0
        self.stream = sys.stderr

    def start(self):
        sys.stdout.flush()    # make sure to not interleave stdout/stderr
        self.stream.write('[')
        self.stream.flush()

    def __call__(self, chunks_so_far, chunk_size, total_size):
        if total_size == -1:  # we do not know size
            n = 0 if chunks_so_far == 0 else self.length / 2
        else:
            n = chunks_so_far * chunk_size * self.length / total_size
        if n > self.length: 
            # If there is a Content-Length, this will be sent as the last progress
            return
        # n ranges from 0 to length*total (exclude), so we'll print at most length dots
        if n >= self.progress:
            self.stream.write('.' * (n-self.progress))
            self.stream.flush()
        self.progress = n
        
    def stop(self):
        missing = '.' * (self.length - self.progress)
        self.stream.write(missing + ']\n')
        self.stream.flush()

    def error_stop(self):
        missing = 'x' * (self.length - self.progress)
        self.stream.write(missing + ']\n')
        self.stream.flush()
        

def http_download(url, destination=None, progress=True):
    """
    Download via HTTP

    INPUT:

    - ``url`` -- string. The URL to download.

    - ``destination`` -- string or ``None`` (default). The destination
      file name to save to. If not specified, the file is written to
      stdout.

    - ``progress`` -- boolean (default: ``True``). Whether to print a
      progress bar to stderr.
    """
    if destination is None:
        destination = '/dev/stdout'
    opener = urllib.FancyURLopener()
    opener.http_error_default = http_error_default
    if progress:
        progress_bar = ProgressBar()
        progress_bar.start()
        try:
            filename, info = opener.retrieve(url, destination, progress_bar)
        except IOError:
            progress_bar.error_stop()
            raise
        else:
            progress_bar.stop()
    else:
        filename, info = opener.retrieve(url, destination)


class MirrorList(object):
    """
    List of mirrors, ranked by speed

    EXAMPLES::

        >>> from sage_pkg.mirror_network import MirrorList
        >>> mirror_list = MirrorList()   # doctest: +ELLIPSIS
        ...
        >>> for mirror in mirror_list: 
        ...     print(mirror)
        http://try.this.first/packages
        http://download.example.com/packages
    """


    MAXAGE = 24*60*60   # seconds

    @property
    def mirror_list_url(self):
        return config('mirrors', 'list', default=None)

    @property
    def filename(self):
        return os.path.join(config.path.download_cache, 'mirror_list')

    def __init__(self):
        if self.mirror_list_url is None:
            self.mirrors = []
        elif self.must_refresh():
            print('Downloading the mirror list')
            with contextlib.closing(urllib.urlopen(self.mirror_list_url)) as f:
                mirror_list = f.read()
            self.mirrors = self._load(mirror_list)
            self._rank_mirrors()
            self._save()
        else:
            self.mirrors = self._load()

    def _load(self, mirror_list = None):
        """
        Load and return `mirror_list` (defaults to the one on disk) as
        a list of strings
        """
        if mirror_list is None:
            with open(self.filename, 'rt') as f:
                mirror_list = f.read()
        import ast
        return ast.literal_eval(mirror_list)

    def _save(self):
        """
        Save the mirror list for (short-term) future  use.
        """
        with open(self.filename, 'wt') as f:
            f.write(repr(self.mirrors))

    def _port_of_mirror(self, mirror):
        if mirror.startswith('http://'):
            return 80
        if mirror.startswith('https://'):
            return 443
        if mirror.startswith('ftp://'):
            return 21

    def _rank_mirrors(self):
        """
        Sort the mirrors by speed, fastest being first

        This method is used by the YUM fastestmirror plugin 
        """
        timed_mirrors = []
        import time, socket
        print('Searching fastest mirror')
        timeout = 1
        for mirror in self.mirrors:
            port = self._port_of_mirror(mirror)
            mirror_hostname = urlparse.urlsplit(mirror).netloc
            time_before = time.time()
            try:
                sock = socket.create_connection((mirror_hostname, port), timeout)
                sock.close()
            except (IOError, socket.error, socket.timeout):
                continue
                print(str('ERROR').rjust(5) + '    ' + mirror)
            result = time.time() - time_before
            result_ms = int(1000 * result)
            print(str(result_ms).rjust(5) + 'ms: ' + mirror)
            timed_mirrors.append((result, mirror))
        timed_mirrors.sort()
        self.mirrors = [m[1] for m in timed_mirrors]
        print('Fastest mirror: ' + self.mirrors[0])

    @property
    def fastest(self):
        return self.mirrors[0]

    def age(self):
        """
        Return the age of the cached mirror list in seconds
        """
        import time
        mtime = os.path.getmtime(self.filename)
        now = time.mktime(time.localtime())
        return now - mtime

    def must_refresh(self):
        """
        Return whether we must download the mirror list.

        If and only if this method returns ``False`` is it admissible
        to use the cached mirror list.
        """
        if not os.path.exists(self.filename):
            return True
        return self.age() > self.MAXAGE

    def __iter__(self):
        """
        Iterate through the list of mirrors.

        This is the main entry point into the mirror list. Every
        script should just use this function to try mirrors in order
        of preference. This will not just yield the official mirrors,
        but also urls for packages that are currently being tested.
        """
        for mirror in config('mirrors', 'first', default=[]):
            yield mirror
        for mirror in self.mirrors:
            yield mirror
        for mirror in config('mirrors', 'extra', default=[]):
            yield mirror


class ChecksumError(Exception):
    pass

class FileNotMirroredError(Exception):
    pass


class Tarball(object):
    
    def __init__(self, tarball_name, sha1=None):
        """
        A (third-party downloadable) tarball

        INPUT:

        - ``name`` - string. The full filename (``foo-1.3.tar.bz2``)
          of a tarball on the Sage mirror network.
        """
        self.filename = tarball_name
        self.base, self.verson, self.ext = self._parse_name(tarball_name)
        self.sha1 = sha1

    @property
    def package(self):
        """
        Return the package name (the subdirectory of ``build/pkgs/``)
        """
        return self.base.lower()

    @property
    def upstream_fqn(self):
        """
        The fully-qualified (including directory) file name in the upstream directory.
        """
        return os.path.join(config.path.download_cache, self.filename)

    def _parse_name(self, name):
        """
        Parse the tarball name into base, version, and extension
        """
        import re
        regex = re.compile('(?P<base>(?:[^-]|-(?!\d))*)-(?P<version>.*)\.(?P<ext>tar.*|zip|tgz)')
        match = regex.match(name)
        if not match:
            raise ValueError('%s does not in tarball name format "xyz-1.0.tar.gz"', name)
        return match.groups()

    def _compute_hash(self, algorithm):
        with open(self.upstream_fqn, 'rb') as f:
            while True:
                buf = f.read(0x100000)
                if not buf:
                    break
                algorithm.update(buf)
        return algorithm.hexdigest()

    def _compute_sha1(self):
        import hashlib
        return self._compute_hash(hashlib.sha1())

    def checksum_verifies(self):
        """
        Test whether the checksum of the downloaded file is correct.
        """
        sha1 = self._compute_sha1()
        return sha1 == self.sha1

    def is_cached(self):
        return os.path.isfile(self.upstream_fqn) and self.checksum_verifies()

    def download(self, mirror_list):
        """
        Download the tarball to the upstream directory.

        Checksum is verified if the ``sha1`` was given to the
        :class:`Tarball` constructor.
        """
        destination = self.upstream_fqn
        if self.sha1 and os.path.isfile(destination):
            if self.checksum_verifies():
                print('Using cached file {destination}'.format(destination=destination))
                return
            else:
                # Garbage in the upstream directory? Delete and re-download
                print('Invalid checksum for cached file {destination}'.format(destination=destination))
                os.remove(destination)
        successful_download = False
        for mirror in mirror_list:
            mirror = mirror.rstrip('/')
            url =  '/'.join([mirror, 'upstream', self.package, self.filename])
            print(url)
            try:
                http_download(url, self.upstream_fqn)
                successful_download = True
                break
            except IOError:
                pass  # mirror doesn't have file for whatever reason...
        if not successful_download:
            raise FileNotMirroredError('tarball does not exist on mirror')
        if self.sha1 and not self.checksum_verifies():
            raise ChecksumError('checksum does not match')

    def save_as(self, destination):
        import shutil
        shutil.copy(self.upstream_fqn, destination)



if __name__ == '__main__':
    progress = True
    url = None
    destination = None
    for arg in sys.argv[1:]:
        if arg.startswith('--quiet'):
            progress = False
            continue
        if url is None:
            url = arg
            continue
        if destination is None:
            destination = arg
            continue
        raise ValueError('too many arguments')
    if url is None:
        print(usage)
        sys.exit(1)
    if url.startswith('http://') or url.startswith('https://') or url.startswith('ftp://'):
        http_download(url, destination, progress=progress)
    else:
        # url is a tarball name
        mirror_list = MirrorList()
        tarball = Tarball(url)
        tarball.download(mirror_list)
        if destination is not None:
            tarball.save_as(destination)
