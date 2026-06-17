using Application.Services.Interfaces;
using AutoMapper;
using Domain.DTOs;
using Domain.Entities;
using Domain.Interfaces;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Application.Services.Implementations
{
    public class CityService : ICityService
    {
        private readonly ICityRepository _cityRepository;
        private readonly IMapper _mapper;

        #region Constructor
        public CityService(ICityRepository cityRepository, IMapper mapper)
        {
            _cityRepository = cityRepository;
            _mapper = mapper;
        }

        public async Task AddCityAsync(CreateCityDto createCityDto)
        {
            string? imagePath = null;
            if (createCityDto.Image != null)
            {
                imagePath = await UploadImageAsync(createCityDto.Image);
            }

            var city = new City()
            {
                Name = createCityDto.Name,
                ImageUrl = imagePath
            };

            await _cityRepository.AddCityAsync(city);
            await _cityRepository.SaveChangesAsync();
        }


        #endregion
        public async Task<IEnumerable<CityDto>> GetAllCitiesAsync()
        {
            var cities = await _cityRepository.GetAllCitiesAsync();
            return _mapper.Map<IEnumerable<CityDto>>(cities);
        }

        public async Task<CityDto?> GetCityByCityIdAsync(int cityId)
        {
            var city = await _cityRepository.GetCityByCityIdAsync(cityId);
            return _mapper.Map<CityDto?>(city);
        }

        private async Task<string> UploadImageAsync(IFormFile image)
        {
            var folder =
                Path.Combine(Directory.GetCurrentDirectory(), "wwwroot/images/cities");

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

            return "/images/cities/" + fileName;
        }
    }
}
