import os
import sys
import errno

from fuse import FUSE, FuseOSError, Operations


class GDBFSFuse(Operations):
    def __init__(self, root):
        self.root = root

    # Helpers
    # =======

    def _full_path(self, partial):
        if partial.startswith("/"):
            partial = partial[1:]
        path = os.path.join(self.root, partial)
        return path

    # Filesystem methods
    # ==================

    def access(self, path, mode):
        print('[access] {}'.format(path))
        full_path = self._full_path(path)
        if not os.access(full_path, mode):
            raise FuseOSError(errno.EACCES)

    def chmod(self, path, mode):
        print('[chmod] {}'.format(path))
        full_path = self._full_path(path)
        return os.chmod(full_path, mode)

    def chown(self, path, uid, gid):
        print('[chown] {}'.format(path))
        full_path = self._full_path(path)
        return os.chown(full_path, uid, gid)

    def getattr(self, path, fh=None):
        full_path = self._full_path(path)
        st = os.lstat(full_path)
        return dict((key, getattr(st, key)) for key in ('st_atime', 'st_ctime',
                                                        'st_gid', 'st_mode', 'st_mtime', 'st_nlink', 'st_size',
                                                        'st_uid'))

    def readdir(self, path, fh):
        print('[readdir] {}'.format(path))
        full_path = self._full_path(path)

        dirents = ['.', '..']
        if os.path.isdir(full_path):
            dirents.extend(os.listdir(full_path))
        for r in dirents:
            yield r

    def readlink(self, path):
        print('[readlink] {}'.format(path))
        pathname = os.readlink(self._full_path(path))
        if pathname.startswith("/"):
            # Path name is absolute, sanitize it.
            return os.path.relpath(pathname, self.root)
        else:
            return pathname

    def mknod(self, path, mode, dev):
        print('[mknod] {}'.format(path))
        return os.mknod(self._full_path(path), mode, dev)

    def rmdir(self, path):
        print('[rmdir] {}'.format(path))
        full_path = self._full_path(path)
        return os.rmdir(full_path)

    def mkdir(self, path, mode):
        print('[mkdir] {}'.format(path))
        return os.mkdir(self._full_path(path), mode)

    def statfs(self, path):
        print('[statfs] {}'.format(path))
        full_path = self._full_path(path)
        stv = os.statvfs(full_path)
        return dict((key, getattr(stv, key)) for key in ('f_bavail', 'f_bfree',
                                                         'f_blocks', 'f_bsize', 'f_favail', 'f_ffree', 'f_files',
                                                         'f_flag',
                                                         'f_frsize', 'f_namemax'))

    def unlink(self, path):
        print('[unlink] 删除结点(及其相邻无效了的关键词结点) {}'.format(path))
        return os.unlink(self._full_path(path))

    def symlink(self, target, name):
        print('[symlink] target: {}, name: {}'.format(target, name))
        return os.symlink(self._full_path(target), self._full_path(name))

    def rename(self, old, new):
        print('[rename] 应该更新文件名 {} -> {}'.format(old, new))
        return os.rename(self._full_path(old), self._full_path(new))

    def link(self, target, name):
        print('[link] target: {}, name: {}'.format(target, name))
        return os.link(self._full_path(target), self._full_path(name))

    def utimens(self, path, times=None):
        print('[utimens] {}'.format(path))
        return os.utime(self._full_path(path), times)

    # File methods
    # ============

    def open(self, path, flags):
        print('[open] {}'.format(path))
        full_path = self._full_path(path)
        return os.open(full_path, flags)

    def create(self, path, mode, fi=None):
        print('[create] {}'.format(path))
        full_path = self._full_path(path)
        return os.open(full_path, os.O_WRONLY | os.O_CREAT, mode)

    def read(self, path, length, offset, fh):
        print('[read] {}'.format(path))
        os.lseek(fh, offset, os.SEEK_SET)
        return os.read(fh, length)

    def write(self, path, buf, offset, fh):
        print('[write] 记录文件{}写的动作(后面flush再更新)'.format(path))
        os.lseek(fh, offset, os.SEEK_SET)
        return os.write(fh, buf)

    def truncate(self, path, length, fh=None):
        print('[truncate] {}'.format(path))
        full_path = self._full_path(path)
        with open(full_path, 'r+') as f:
            f.truncate(length)

    def flush(self, path, fh):
        print('[flush] 检查文件{}有没有经历过write, 若有, 更新.'.format(path))
        return os.fsync(fh)

    def release(self, path, fh):
        print('[release] {}'.format(path))
        return os.close(fh)

    def fsync(self, path, fdatasync, fh):
        print('[fsync] {}'.format(path))
        return self.flush(path, fh)


def mount_gdbfs(mountpoint):
    FUSE(GDBFSFuse('./sample_files'), mountpoint, foreground=True)


if __name__ == '__main__':
    mount_gdbfs(sys.argv[1])
