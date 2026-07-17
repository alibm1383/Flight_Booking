using Application.Services.Interfaces;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public class FileService : IFileService
    {
        public async Task<string> UploadImageAsync(IFormFile image, string folderName)
        {
            var folder =
                Path.Combine(Directory.GetCurrentDirectory(), $"wwwroot/images/{folderName}");

            if (!Directory.Exists(folder))
            {
                Directory.CreateDirectory(folder);
            }

            var fileName = Guid.NewGuid() + Path.GetExtension(image.FileName);

            var path = Path.Combine(folder, fileName);

            using (var stream = new FileStream(path, FileMode.Create))
            {
                await image.CopyToAsync(stream);
            }

            return $"/images/{folderName}/" + fileName;
        }
    }
}
