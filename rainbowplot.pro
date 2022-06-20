function displayrange, xi, margin=margin
  x=xi.finite()
  if not keyword_set(margin) then margin = 0.1 ;ten percent
  xrange=[x.min(),x.max()] + margin*[-1,1]*(x.max()-x.min())
  return, xrange
end


function rainbowerrorplot, x,data,xerr,yerr,format,  $
                           colors=colors, $
                           bc=bc,$
                           yrange=yrange, $
                           xrange=xrange, $
                           cbar=cbar,$
                           show=show, $
                           transpose=transpose,$
                           _EXTRA=ex

  xn=x
  datan=data
  
  if n_params() eq 4 then begin
    if isa(yerr,'String') then begin ;if yerr is a string
      format=yerr
      yerrn=xerr
      xerrn=intarr(yerr.dim)
    endif else begin
      format=' D'
      yerrn=yerr
      xerrn=xerr
    endelse
  endif else if n_params() eq 3 then begin
    format=' D'
    yerrn=xerr
    xerrn=intarr(yerr.dim)
  endif else begin
    xn = x
    datan = data
    xerrn = xerr
    yerrn = yerr
  endelse

  if keyword_set(transpose) then begin
    xn = transpose(xn)
    datan = transpose(datan)
    xerrn = transpose(xerrn)
    yerrn = transpose(yerrn)
  endif  

  ny = (datan.dim)[1]



  if not keyword_set(colors) then begin
    ct=colortable(33)
    colorindices=indgen(ny)*((ct.dim)[0]-1)/(ny-1)
    colors=ct[colorindices,*]
  endif
    
  if not keyword_set(bc) then bc = [1,1,1]*210
  if not keyword_set(yrange) then yrange=displayrange([datan+yerrn,datan-yerrn])
  if not keyword_set(xrange) then begin
    xrange=displayrange([xn+xerrn,xn-xerrn])
  endif
  if not keyword_set(show) then show= ~boolarr(ny)

  
  pl=errorplot([0],[0],[0],[0],format, color=c,errorbar_color=c, $
    background_color=bc, yrange=yrange, xrange=xrange, _EXTRA=ex)
  for i = 0,(ny-1) do begin
    if show[i] then begin
      c=reform(colors[i,*])
      pl=errorplot(xn[*,i],datan[*,i],xerrn[*,i],yerrn[*,i],format, color=c,errorbar_color=c, /overplot,$
        background_color=bc, yrange=yrange, xrange=xrange, _EXTRA=ex)
    endif
  endfor

  if keyword_set(cbar) then begin
    cb=colorbar(target=pl, rgb_table=colors,tickname=[''],major=0,minor=0,orientation=1)
  endif

  return, pl

end

function rainbowplot, x,data,format, $
                      colors=colors, $
                      bc=bc, $
                      yrange=yrange, $
                      xrange=xrange, $
                      cbar=cbar, $
                      show=show, $
                      transpose=transpose,$
                      _EXTRA=ex 
  

  if n_params() lt 3 then format=''
  
  if n_params() eq 1 then begin
    datan = x
    ny = (data.dim)[1]
    nx = (data.dim)[0]
    xn = (indgen(nx)) # (intarr(ny)+1)
  endif else begin
    if (x.ndim) eq 1 then begin
      ny = (data.dim)[1]
      xn = x # (intarr(ny)+1)
    endif else begin
      xn = x
    endelse
    datan = data
  endelse
  
  if keyword_set(transpose) then begin
    xn = transpose(xn)
    datan = transpose(datan)
  endif
  
  ny = (datan.dim)[1]

  if not keyword_set(colors) then begin
    ct=colortable(33)
    colorindices=indgen(ny)*((ct.dim)[0]-1)/(ny-1)
    colors=ct[colorindices,*]
  endif
  
  if not keyword_set(bc) then bc = [1,1,1]*210
  if not keyword_set(yrange) then yrange=displayrange(datan)
  if not keyword_set(xrange) then xrange=displayrange(xn)
  if not keyword_set(show) then show= ~boolarr(ny)

  pl=plot([0],[0],'',background_color=bc, yrange=yrange, $
                     xrange=xrange, _EXTRA=ex)
  for i = 0,(ny-1) do begin
    if show[i] then begin
      c=reform(colors[i,*])
      pl=plot(xn[*,i],datan[*,i],format, color=c, /overplot, _EXTRA=ex)
    endif
  endfor

  if keyword_set(cbar) then begin
    cb=colorbar(target=pl, rgb_table=colors,tickname=[''],major=0,minor=0,orientation=1)
  endif

  return, pl

end

;pro rainbowplot, x,data, yrange=yrange, colors=colors
;  ny = (data.dim)[1]
;
;  if not keyword_set(colors) then begin
;    ct=colortable(34)
;    colors=ct[indgen(ny)*(ct.dim)[0]/ny,*]
;  endif
;
;  pl=plot(x[*,0],data[*,0], color=reform(ct[0,*]), yrange=yrange)
;  for i = 1,(ny-1) do begin
;    pl=plot(x[*,i],data[*,i], color=reform(colors[i,*]), /overplot)
;  endfor
;
;
;
;end
