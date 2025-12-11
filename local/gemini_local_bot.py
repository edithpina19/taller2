<script>
// --- Valores Fijos de Simulación (Aumentamos el valor base para que el cambio sea visible) ---
const TAMANO_BASE_KB = 550; // 550 KB de transferencia (Valor fijo)
const CO2_BASE_POR_VISITA = 0.003; // G CO₂e (¡Cambiado de 0.00003 a 0.003 para ver variación!)

window.onload = function () {
    
    // --- 1. Generar Variación Aleatoria Notable ---
    const rango_variacion = 0.30; // 30% total de rango (-15% a +15%)
    const factor_aleatorio = 1 + (Math.random() - 0.5) * rango_variacion; 

    // --- 2. Aplicar la Variación a los Datos de CO₂ ---
    let co2 = CO2_BASE_POR_VISITA * factor_aleatorio;
    co2 = Math.max(0, co2); 
    const co2Month = co2 * 1000;

    // --- 3. Actualizar la Interfaz (DOM) ---

    document.getElementById("dataSize").textContent = TAMANO_BASE_KB.toFixed(2) + " KB";
    
    // Aumentamos a 8 decimales para que el cambio sea visible en la interfaz
    document.getElementById("co2").textContent = co2.toFixed(8); 
    document.getElementById("co2Month").textContent = co2Month.toFixed(2);

    dibujarGrafica(co2, co2Month);
};

// La función para dibujar la gráfica
function dibujarGrafica(co2, co2Month) {
    const canvas = document.getElementById("grafica");
    const ctx = canvas.getContext("2d");
    canvas.width = canvas.offsetWidth;
    canvas.height = 240;

    const valores = [co2 || 0.00001, co2Month || 0.01]; 
    const etiquetas = ["Por visita", "1000 visitas"];
    const maxValor = Math.max(...valores) || 1;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    valores.forEach((valor, i) => {
        const altura = (valor / maxValor) * 160;
        const x = 90 + i * 200;
        const y = canvas.height - altura - 30;

        ctx.fillStyle = "#16a34a";
        ctx.fillRect(x, y, 100, altura);

        ctx.fillStyle = "#065f46";
        // Mostrar el valor encima de la barra (con el formato correcto de decimales)
        // Usamos 8 decimales para el valor por visita
        const decimales = i === 0 ? 8 : 2; 
        const valorTexto = valor.toFixed(decimales) + ' g CO₂e';
        ctx.fillText(valorTexto, x, y - 5); 
        ctx.fillText(etiquetas[i], x, canvas.height - 10);
    });
}
</script>
