/**
 * 加载博客数据可视化组件
 */
(function() {
  'use strict';
  
  function loadBlogDataWidget() {
    // 检查是否已加载
    if (document.getElementById('card-blog-data')) {
      return; // 避免重复加载
    }
    
    fetch('/js/blog-data-widget.html')
      .then(response => {
        if (!response.ok) throw new Error('HTTP error ' + response.status);
        return response.text();
      })
      .then(html => {
        // 找到侧边栏容器并插入组件
        const asideContent = document.getElementById('aside-content');
        if (asideContent) {
          // 创建临时容器解析 HTML
          const tempDiv = document.createElement('div');
          tempDiv.innerHTML = html;
          
          // 将组件插入到侧边栏末尾
          const widget = tempDiv.firstElementChild;
          if (widget) {
            asideContent.appendChild(widget);
            console.log('✅ 博客数据可视化组件加载成功');
          }
        }
      })
      .catch(error => {
        console.warn('⚠️ 数据组件加载失败:', error.message);
      });
  }
  
  // 页面加载完成后执行
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadBlogDataWidget);
  } else {
    loadBlogDataWidget();
  }
  
  // 如果使用 PJAX，需要在页面切换后重新加载
  if (window.pjax) {
    document.addEventListener('pjax:complete', loadBlogDataWidget);
  }
})();
