document.querySelectorAll('.rectangle').forEach(rectangle => {
    rectangle.addEventListener('click', async () => {
        const section = rectangle.querySelector('h1').textContent.trim().toLowerCase();

        let categoriaNombre = '';
        if (section === 'historia') categoriaNombre = 'Historia';
        else if (section === 'conceptos') categoriaNombre = 'Conceptos';
        else if (section === 'recursos') categoriaNombre = 'Recursos';

        try {
            const response = await fetch(`/api/articulos/${categoriaNombre}/`);
            const data = await response.json();

            const modalTitle = document.getElementById('modalTitle');
            const modalText = document.getElementById('modalText');
            modalTitle.textContent = categoriaNombre;
            modalText.innerHTML = ''; // Limpia contenido previo

            // Llenamos el modal según el tipo
            if (section === 'historia' && data.history.length > 0) {
                data.history.forEach(art => {
                    modalText.innerHTML += `<h3>${art.titulo}</h3><p>${art.contenido.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>')}</p><br><br>`;
                });
            } else if (section === 'conceptos' && data.concepts.length > 0) {
                data.concepts.forEach(art => {
                    modalText.innerHTML += `<h3>${art.titulo}</h3><p>${art.contenido.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>')}</p><br><br>`;
                });
            } else if (section === 'recursos') {
                const recursos = data.resources;

                // Crear pestañas
                modalText.innerHTML += `
                    <div class="tabs">
                        <button class="tab-button active" data-tab="libros">Libros</button>
                        <button class="tab-button" data-tab="canales">Canales de Youtube</button>
                        <button class="tab-button" data-tab="webs">Páginas Web</button>
                    </div>
                    <div class="tab-content-container">
                        <div class="tab-content active" id="tab-libros"></div>
                        <div class="tab-content" id="tab-canales"></div>
                        <div class="tab-content" id="tab-webs"></div>
                    </div>
                `;

                for (const tipo in recursos) {
                    const container = document.getElementById(`tab-${tipo}`);
                    recursos[tipo].forEach(art => {
                        container.innerHTML += `
                            <div class="resource-card">
                                <h4>${art.titulo}</h4>
                                <p>${art.contenido.replace(/\n\n/g, '</p><p>').replace(/\n/g, '<br>')}</p>
                                <a href="${art.url}" target="_blank">Ver recurso</a>
                            </div>
                        `;
                    });
                }
            }

            // Event listeners para pestañas
            document.querySelectorAll('.tab-button').forEach(btn => {
                btn.addEventListener('click', () => {
                    // Quitar clase 'active' a todas
                    document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
                    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

                    // Activar la pulsada
                    btn.classList.add('active');
                    document.getElementById(`tab-${btn.dataset.tab}`).classList.add('active');
                });
            });

            document.getElementById('infoModal').style.display = 'block';

        } catch (error) {
            console.error('Error al cargar artículos:', error);
            alert('Hubo un error al cargar los contenidos.');
        }
    });
});

// Cerrar el modal al hacer clic en la flecha
document.getElementById('closeModal').addEventListener('click', () => {
    document.getElementById('infoModal').style.display = 'none';
});
