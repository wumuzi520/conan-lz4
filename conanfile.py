from conans import ConanFile, AutoToolsBuildEnvironment, tools, os

class LZ4Conan(ConanFile):
    name = "LZ4"
    version = "1.8.0"
    description = "Extremely Fast Compression algorithm"
    license = "https://github.com/lz4/lz4/blob/master/lib/LICENSE"
    url = "https://github.com/bincrafters/conan-lz4"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "with_msys": [True, False]}
    default_options = "shared=False", "with_msys=True"
    lib_short_name = "lz4"
    archive_name = "{0}-{1}".format(lib_short_name, version)
    
    def configure(self):
        if self.settings.os != "Windows":
            self.options.with_msys = "False"

    def build_requirements(self):
        if self.options.with_msys:
            self.build_requires("msys2_installer/latest@bincrafters/stable")
        elif self.settings.os == 'Windows' and 'MSYS_ROOT' not in os.environ:
            raise Exception("MSYS_ROOT environment variable must exist if with_msys=False.") 
            
    def source(self):
        source_url = "https://github.com/lz4/lz4"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        os.rename(self.archive_name, "sources")

    def _run_cmd(self, command):
        with tools.chdir("sources"):
            if self.settings.os == "Windows":
                tools.run_in_windows_bash(self, command)
            else:
                self.run(command)
         
    def build(self):
        # if self.settings.os == "Windows":
        # sln = os.path.join(self.archive_name, "visual", "vs2010", "lz4.sln")
        # if self.options.shared:
            # target = "liblz4-dll"
        # else: 
            # target = "liblz4"
        # vcvars_cmd = tools.vcvars_command(self.settings)
        # build_cmd = tools.msvc_build_command(self.settings, sln_path=sln , targets=[target])
        # build_cmd = build_cmd.replace('"x86"', '"Win32"')
        # self.run("{0} && {1}".format(vcvars_cmd, build_cmd))
        env_build = AutoToolsBuildEnvironment(self)
        with tools.environment_append(env_build.vars):
            self._run_cmd("make")
         
    def package(self):

        # # yes, headers are in lib
        # include_dir = os.path.join("%s-%s" % ( self.name, self.version ), 'lib')

        # self.copy(pattern="lz4*.h", dst="include", src=include_dir, keep_path=False)
        # self.copy("*.dll", dst="bin", keep_path=False)
        # self.copy("*.so*", dst="lib", keep_path=False)
        # self.copy("*.dylib", dst="lib", keep_path=False)
        # self.copy("*.a", dst="lib", keep_path=False)
        # self.copy("*.lib", dst="lib", keep_path=False)
        self.run("make install")
            
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
