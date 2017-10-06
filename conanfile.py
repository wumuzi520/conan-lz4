from conans import ConanFile, tools, os

class LZ4Conan(ConanFile):
    name = "LZ4"
    version = "1.8.0"
    description = "Extremely Fast Compression algorithm"
    license = "https://github.com/lz4/lz4/blob/master/lib/LICENSE"
    url = "https://github.com/bincrafters/conan-lz4"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=True"
    lib_short_name = "lz4"
    archive_name = "{0}-{1}".format(lib_short_name, version)
            
    def source(self):
        source_url = "https://github.com/lz4/lz4"
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
                
    def build(self):
        if self.settings.os == "Windows":
            sln = os.path.join(self.archive_name, "visual", "vs2010", "lz4.sln")
            if self.options.shared:
                target = "liblz4"
            else: 
                target = "liblz4-dll"
            vcvars_cmd = tools.vcvars_command(self.settings)
            build_cmd = tools.msvc_build_command(self.settings, sln_path=sln , targets=[target])
            platform_toolset = {'14': 'vs140', '15':  'vs140'}[str(self.settings.compiler.version)]
            self.run("{0} && {1} /property:PlatformToolset={2}".format(vcvars_cmd, build_cmd, platform_toolset))
        #if self.settings.os == "Linux":
        #if self.settings.os == "Darwin":
       
    
    def package(self):
        self.copy("*.h", dst="include", src=os.path.join(self.lib_short_name, "include"))
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so*", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)
        self.copy("*.lib", dst="lib", keep_path=False)
            
    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
