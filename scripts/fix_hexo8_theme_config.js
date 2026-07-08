const { deepMerge } = require('hexo-util')

hexo.extend.filter.register('before_generate', () => {
  const { theme_config } = hexo.config
  if (theme_config && typeof theme_config === 'object') {
    hexo.theme.config = deepMerge(hexo.theme.config, theme_config)
  }
}, 0)
