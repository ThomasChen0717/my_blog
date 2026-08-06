/**
 * Matrix Code Rain Effect - Super Bright
 * 超亮多彩代码雨背景
 */

(function() {
    const canvas = document.getElementById('matrix-canvas');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');

    // 代码字符集
    const chars = '01ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789{}[]()<>/*+-=;:$#@你好世界';
    const charArray = chars.split('');

    // 多种颜色方案 - 更亮的颜色
    const colorSchemes = [
        { r: 0, g: 255, b: 120 },   // 霓虹绿
        { r: 0, g: 230, b: 255 },   // 赛博青
        { r: 200, g: 120, b: 255 }, // 梦幻紫
        { r: 255, g: 100, b: 220 }, // 霓虹粉
        { r: 255, g: 220, b: 80 },  // 霓虹黄
    ];

    // 字体大小和列数
    const fontSize = 16;
    let columns = Math.floor(window.innerWidth / fontSize);
    let drops = Array(columns).fill(1);
    let columnColors = Array(columns).fill(0).map(() => 
        colorSchemes[Math.floor(Math.random() * colorSchemes.length)]
    );

    // 设置画布大小
    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        columns = Math.floor(canvas.width / fontSize);
        drops = Array(columns).fill(1);
        columnColors = Array(columns).fill(0).map(() => 
            colorSchemes[Math.floor(Math.random() * colorSchemes.length)]
        );
    }

    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    // 绘制函数
    function draw() {
        // 拖尾效果
        ctx.fillStyle = 'rgba(8, 8, 16, 0.12)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        // 绘制字符
        for (let i = 0; i < drops.length; i++) {
            const text = charArray[Math.floor(Math.random() * charArray.length)];
            const x = i * fontSize;
            const y = drops[i] * fontSize;

            const color = columnColors[i];
            
            // 亮度范围 0.7 - 1.0 (之前错误地超过了1)
            const alpha = Math.random() * 0.3 + 0.7;

            // 主字符
            ctx.fillStyle = `rgba(${color.r}, ${color.g}, ${color.b}, ${alpha})`;
            ctx.font = `bold ${fontSize}px 'Consolas', monospace`;
            ctx.shadowColor = `rgba(${color.r}, ${color.g}, ${color.b}, 0.9)`;
            ctx.shadowBlur = 10;
            ctx.fillText(text, x, y);

            // 头部白色高亮
            if (Math.random() > 0.94) {
                ctx.fillStyle = `rgba(255, 255, 255, ${alpha})`;
                ctx.shadowColor = `rgba(255, 255, 255, 1)`;
                ctx.shadowBlur = 15;
                ctx.fillText(text, x, y);
            }

            // 偶尔切换列颜色
            if (Math.random() > 0.995) {
                columnColors[i] = colorSchemes[Math.floor(Math.random() * colorSchemes.length)];
            }

            // 重置或继续下落
            if (y > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
                if (Math.random() > 0.5) {
                    columnColors[i] = colorSchemes[Math.floor(Math.random() * colorSchemes.length)];
                }
            }
            drops[i]++;
        }
        
        ctx.shadowBlur = 0;
    }

    // 随机化起始位置
    for (let i = 0; i < drops.length; i++) {
        drops[i] = Math.random() * -50;
    }

    // 启动动画
    setInterval(draw, 40);
})();
