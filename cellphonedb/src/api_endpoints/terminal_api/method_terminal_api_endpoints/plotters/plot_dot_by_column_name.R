
dot_plot = function(selected_rows = NULL, selected_columns = NULL, filename = 'plot.pdf', width = 8, height = 10){

  all_pval = read.table('pvalues.txt', header=T, stringsAsFactors = F, sep='\t', comment.char = '')
  all_means = read.table('means.txt', header=T, stringsAsFactors = F, sep='\t', comment.char = '')

  rownames(all_pval) = all_pval$interacting_pair
  rownames(all_means) = all_means$interacting_pair
  all_pval = all_pval[,-c(1:9)]
  all_means = all_means[,-c(1:9)]

  if(is.null(selected_rows) || is.null(selected_columns)){
    selected_rows = rownames(all_pval)
    selected_columns = colnames(all_pval)
  }

  sel_pval = all_pval[selected_rows, selected_columns]
  sel_means = all_means[selected_rows, selected_columns]

  df_names = expand.grid(rownames(sel_pval), colnames(sel_pval))
  pval = unlist(sel_pval)
  pval[pval==0] = 0.0009
  plot.data = cbind(df_names,pval)
  pr = unlist(as.data.frame(sel_means))
  pr[pr==0] = 1
  plot.data = cbind(plot.data,log2(pr))
  colnames(plot.data) = c('pair', 'clusters', 'pvalue', 'mean')

  my_palette <- colorRampPalette(c("black", "blue", "yellow", "red"), alpha=TRUE)(n=399)

  ggplot(plot.data,aes(x=clusters,y=pair)) +
  geom_point(aes(size=-log10(pvalue),color=mean)) +
  scale_color_gradientn('Log2 mean (Molecule 1, Molecule 2)', colors=my_palette) +
  theme_bw() +
  theme(panel.grid.minor = element_blank(),
        panel.grid.major = element_blank(),
        axis.text=element_text(size=14, colour = "black"),
        axis.text.x = element_text(angle = 90, hjust = 1, family = 'Arial'),
        axis.text.y = element_text(size=12, colour = "black", family = 'Arial'),
        axis.title=element_blank(),
        text = element_text('Arial'),
        panel.border = element_rect(size = 0.7, linetype = "solid", colour = "black"))
  ggsave(filename, width = width, height = height, device = cairo_pdf, limitsize=F)

}

