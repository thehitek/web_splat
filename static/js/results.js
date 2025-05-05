const imageList = [
    { label: "Mountain", query: "mountain" },
    { label: "Beach", query: "beach" },
    { label: "Forest", query: "forest" },
    { label: "Desert", query: "desert" },
    { label: "City", query: "city" }
  ];

  const sidebar = document.getElementById('sidebar');
  const imageEl = document.getElementById('image');

  const fetchImage = async (query) => {
    const response = await fetch(`https://source.unsplash.com/800x600/?${query}`);
    imageEl.src = response.url;
  };

  imageList.forEach(item => {
    const button = document.createElement('button');
    button.textContent = item.label;
    button.addEventListener('click', () => fetchImage(item.query));
    sidebar.appendChild(button);
  });

  // Load first image by default
  fetchImage(imageList[0].query);