from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class LZ4Conan(ConanFile):
    name = "LZ4"
    version = "1.8.0"
    description = "Extremely Fast Compression algorithm"
    license = "https://github.com/lz4/lz4/blob/master/lib/LICENSE"
    url = "https://github.com/bincrafters/conan-lz4"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    lib_short_name = "lz4"
    archive_name = "{0}-{1}".format(lib_short_name, version)
    
    def configure(self):
        pass

    def build_requirements(self):
        pass
            
    def source(self):
        source_url = "https://github.com/lz4/lz4"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        os.rename(self.archive_name, "sources")

    def build_make(self):
        install_dir = os.path.abspath('lz4-install')
        with tools.chdir("sources"):
            env_build = AutoToolsBuildEnvironment(self)
            with tools.environment_append(env_build.vars):
                self.run("make")
                self.run("make DESTDIR=%s install" % install_dir)

    def build_vs(self):
        with tools.chdir(os.path.join('sources', 'visual', 'VS2010')):
            target = 'liblz4-dll' if self.options.shared else 'liblz4'

            if self.settings.compiler.runtime == 'MD':
                runtime = 'MultiThreadedDLL'
            elif self.settings.compiler.runtime == 'MDd':
                runtime = 'MultiThreadedDebugDLL'
            elif self.settings.compiler.runtime == 'MT':
                runtime = 'MultiThreaded'
            elif self.settings.compiler.runtime == 'MTd':
                runtime = 'MultiThreadedDebug'

            path = os.path.join(target, '%s.vcxproj' % target)
            tools.replace_in_file(path, search='</ClCompile>',
                                  replace='<RuntimeLibrary>%s</RuntimeLibrary></ClCompile>' % runtime)

            command = tools.msvc_build_command(self.settings, os.path.join(os.getcwd(), 'lz4.sln'), targets=[target])
            if self.settings.arch == 'x86':
                command = command.replace('/p:Platform="x86"', '/p:Platform="Win32"')
            self.run(command)
         
    def build(self):
        if self.settings.os == "Windows":
            self.build_vs()
        else:
            self.build_make()

    def package(self):
        if self.settings.os == "Windows":
            include_dir = os.path.join('sources', 'lib')
            self.copy(pattern="lz4*.h", dst="include", src=include_dir, keep_path=False)
            arch = 'Win32' if self.settings.arch == 'x86' else 'x64'
            bin_dir = os.path.join('sources', 'visual', 'VS2010', 'bin', '%s_%s' %
                                   (arch, self.settings.build_type))
            if self.options.shared:
                self.copy("*.dll", dst='bin', src=bin_dir, keep_path=False)
            self.copy("*.lib", dst='lib', src=bin_dir, keep_path=False)
        # # yes, headers are in lib
        # include_dir = os.path.join("%s-%s" % ( self.name, self.version ), 'lib')

        # self.copy(pattern="lz4*.h", dst="include", src=include_dir, keep_path=False)
        # self.copy("*.so*", dst="lib", keep_path=False)
        # self.copy("*.dylib", dst="lib", keep_path=False)
        # self.copy("*.a", dst="lib", keep_path=False)
            
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
