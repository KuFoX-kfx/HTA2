async function loaddata(){
    const response = await fetch('hhtp://127.0.0.1.5000/api/data')
    const data = await response.json();

    constdataContainer = document.getElementById('data-container')
    data.images.forEach(image => {
        const imageItem = document.createElement('div');
        imageItem.classList.add('image-item');
        
        const imgElement = document.createElement('img');
        imgElement.src = 'static/uploads/${image.filename}';
        imgElement.alt =image.description;
        imgElement.width = 100;

        const description = document.createElement('p');
        description.textContent = 'Description: ${image.description}';

        const characteristics = document.createElement('p');
        characteristics.textContent = 'characteristics: ${image.characteristics}';

        imageItem.appendChild(imgElement);
        imageItem.appendChild(description);
        imageItem.appendChild(characteristics);

        dataContainer.appendChild(imageItem);

    });
}

window.addEventListener('load', loaddata);